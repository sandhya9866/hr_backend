from django import forms
from utils.date_converter import english_to_nepali, nepali_str_to_english
from .models import FiscalYear
from utils.enums import ACTIVE_INACTIVE, YesNoList

class FiscalYearForm(forms.ModelForm):
    # Override start_date and end_date as CharField to avoid early parsing
    start_date = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'YYYY-MM-DD (BS)', 'class': 'nep_date'
    }))
    end_date = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'YYYY-MM-DD (BS)', 'class': 'nep_date'
    }))

    class Meta:
        model = FiscalYear
        fields = ('fiscal_year', 'start_date', 'end_date', 'status', 'is_current')
        widgets = {
            'fiscal_year': forms.TextInput(attrs={'placeholder': 'Eg:2082/83'}),
            'status': forms.Select(choices=ACTIVE_INACTIVE),
            'is_current': forms.Select(choices=YesNoList),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.start_date:
                self.initial['start_date'] = english_to_nepali(self.instance.start_date)
            if self.instance.end_date:
                self.initial['end_date'] = english_to_nepali(self.instance.end_date)

    def clean(self):
        cleaned_data = super().clean()
        start_date_str = cleaned_data.get('start_date')
        end_date_str = cleaned_data.get('end_date')

        # Convert to English date
        try:
            cleaned_data['start_date'] = nepali_str_to_english(start_date_str)
        except Exception:
            self.add_error('start_date', "Invalid Nepali date format or non-existent date.")

        try:
            cleaned_data['end_date'] = nepali_str_to_english(end_date_str)
        except Exception:
            self.add_error('end_date', "Invalid Nepali date format or non-existent date.")

        # Ensure only one fiscal year is current
        if cleaned_data.get('is_current'):
            existing = FiscalYear.objects.filter(is_current=True)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError("Only one Fiscal Year can be marked as current.")

        return cleaned_data
