from django import forms
from utils.enums import ACTIVE_INACTIVE, YesNoList
from .models import FiscalYear

class FiscalYearForm(forms.ModelForm):
    class Meta:
        model = FiscalYear
        fields = ('fiscal_year', 'start_date', 'end_date', 'status', 'is_current')
        widgets = {
            'fiscal_year': forms.TextInput(attrs={'placeholder': 'Eg:2082/83'}),
            'start_date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD (BS)', 'class': 'nep_date'}),
            'end_date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD (BS)', 'class': 'nep_date'}),
            'status': forms.Select(choices=ACTIVE_INACTIVE),
            'is_current': forms.Select(choices=YesNoList),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_current = cleaned_data.get('is_current')

        if is_current:
            existing = FiscalYear.objects.filter(is_current=True)

            # Exclude current instance in case of editing
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise forms.ValidationError("Only one Fiscal Year can be marked as current.")
