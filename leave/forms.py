from django import forms

from fiscal_year.models import FiscalYear
from .models import Leave, LeaveType

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
        super().__init__(*args, **kwargs)
        self.fields['leave_type'].empty_label = "Select Leave Type"

        # self.fields['fiscal_year'].queryset = FiscalYear.objects.filter(status='active').order_by('-id')

