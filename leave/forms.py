from django import forms
import datetime
from datetime import timedelta
from fiscal_year.models import FiscalYear
from utils.date_converter import english_to_nepali, nepali_str_to_english
from .models import EmployeeLeave, Leave, LeaveType
from django.core.exceptions import ValidationError
from nepali_datetime import date as nep_date


#Leave Type
class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = (
            'fiscal_year', 'name', 'code', 'number_of_days', 'leave_type', 'gender', 'marital_status',
            'description', 'show_on_employee',
            'prorata_status', 'encashable_status', 'half_leave_status',
            'half_leave_type', 'carry_forward_status', 'sandwich_rule_status',
            'pre_inform_days', 'max_per_day_leave', 'status', 'job_type'
        )
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter title'}),
            'code': forms.TextInput(attrs={'placeholder': 'Enter code'}),
            'number_of_days': forms.NumberInput(attrs={'placeholder': 'Enter number of days'}),
            'description': forms.Textarea(attrs={'placeholder': 'Write description here...'}),
            'pre_inform_days': forms.NumberInput(attrs={'placeholder': 'e.g. 3'}),
            'max_per_day_leave': forms.NumberInput(attrs={'placeholder': 'e.g. 2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fiscal_year'].empty_label = "Select Fiscal Year"
        self.fields['fiscal_year'].queryset = FiscalYear.objects.filter(status='active').order_by('-id')

#Leave
class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = (
            'leave_type', 'start_date', 'end_date', 'reason'
        )
        widgets = {
            'start_date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD', 'class': 'nep_date'}),
            'end_date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD', 'class': 'nep_date'}),
            'reason': forms.Textarea(attrs={'placeholder': 'Write reason here...'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)
        self.fields['leave_type'].empty_label = "Select Leave Type"

        if self.user:
            assigned_leave_type_ids = EmployeeLeave.objects.filter(
                employee=self.user,
                leave_type__fiscal_year__is_current=True,
            ).values_list('leave_type_id', flat=True)

            self.fields['leave_type'].queryset = LeaveType.objects.filter(id__in=assigned_leave_type_ids)

    def clean(self):
        cleaned_data = super().clean()
        leave_type = cleaned_data.get('leave_type')

        start_date_nep = self.data.get('start_date')
        end_date_nep = self.data.get('end_date')

        try:
            start_date_eng = nepali_str_to_english(start_date_nep)
            end_date_eng = nepali_str_to_english(end_date_nep)
        except Exception:
            raise ValidationError("Invalid Nepali date format.")

        if end_date_eng < start_date_eng:
            raise ValidationError("End date cannot be before start date.")

        no_of_days = (end_date_eng - start_date_eng).days + 1

        if leave_type:
            #max_per_day_leave check
            if leave_type.max_per_day_leave and no_of_days > leave_type.max_per_day_leave:
                raise ValidationError(
                    f"You cannot take more than {leave_type.max_per_day_leave} days for this leave type."
                )

            #pre_inform_days check
            if leave_type.pre_inform_days:
                today = datetime.date.today()
                days_in_advance = (start_date_eng - today).days
                if days_in_advance < leave_type.pre_inform_days:
                    raise ValidationError(
                        f"You must apply at least {leave_type.pre_inform_days} day(s) in advance."
                    )

        # 3. Check for overlapping leaves with specific dates
        start_nep = nep_date.from_datetime_date(start_date_eng)
        end_nep = nep_date.from_datetime_date(end_date_eng)

        overlapping_leaves = Leave.objects.filter(
            employee=self.user,
            start_date__lte=end_nep,
            end_date__gte=start_nep,
        ).exclude(status__in=['Declined', 'Rejected'])

        # Exclude current instance when editing
        if self.instance and self.instance.pk:
            overlapping_leaves = overlapping_leaves.exclude(pk=self.instance.pk)

        if overlapping_leaves.exists():
            # Create set of requested English dates
            requested_dates = set(start_date_eng + timedelta(days=i) for i in range(no_of_days))
            taken_dates = set()

            for leave in overlapping_leaves:
                # Convert Nepali leave dates to English for accurate comparison
                leave_start_eng = leave.start_date.to_datetime_date()
                leave_end_eng = leave.end_date.to_datetime_date()

                leave_dates = set(
                    leave_start_eng + timedelta(days=i)
                    for i in range((leave_end_eng - leave_start_eng).days + 1)
                )
                taken_dates |= leave_dates

            conflict_dates = sorted(requested_dates & taken_dates)

            if conflict_dates:
                formatted_dates = ', '.join([
                    nep_date.from_datetime_date(date).strftime('%Y-%m-%d')
                    for date in conflict_dates
                ])
                raise ValidationError(f"You have already taken leave on: {formatted_dates}.")


