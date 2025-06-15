from django import forms
from fiscal_year.models import FiscalYear
from payroll.models import SalaryRelease, SalaryType
from user.models import AuthUser
from utils.date_converter import english_to_nepali, nepali_str_to_english

class SalaryTypeForm(forms.ModelForm):
    class Meta:
        model = SalaryType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super(SalaryTypeForm,self).__init__(*args, **kwargs)
        self.fields['name'].required = True


class SalaryReleaseForm(forms.ModelForm):
    start_date = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'YYYY-MM-DD (BS)', 'class': 'nep_date'
    }))
    end_date = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'YYYY-MM-DD (BS)', 'class': 'nep_date'
    }))
    class Meta:
        model = SalaryRelease
        fields = ['employee', 'salary_type', 'start_date', 'end_date', 'fiscal_year', 'month', 'amount', 'no_of_product', 'rate', 'tax', 'net_amount']

    def __init__(self, *args, **kwargs):
        super(SalaryReleaseForm, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset = AuthUser.get_active_users()
        self.fields['fiscal_year'].queryset = FiscalYear.active_fiscal_year_list()
        
        self.fields['employee'].empty_label = "Select Employee"
        self.fields['salary_type'].empty_label = "Select Salary Type"
        self.fields['fiscal_year'].empty_label = "Select Fiscal Year"

         #Convert instance English dates to Nepali for display in the form
        if self.instance and self.instance.pk:
            if self.instance.start_date:
                self.initial['start_date'] = english_to_nepali(self.instance.start_date)
            if self.instance.end_date:
                self.initial['end_date'] = english_to_nepali(self.instance.end_date)

    def clean(self):
        cleaned_data = super(SalaryReleaseForm, self).clean()
        
        start_date_nep_str = cleaned_data.get('start_date')
        end_date_nep_str = cleaned_data.get('end_date')

        # Convert to English date
        try:
            cleaned_data['start_date'] = nepali_str_to_english(start_date_nep_str)
        except Exception:
            self.add_error('start_date', "Invalid Nepali date format or non-existent date.")

        try:
            cleaned_data['end_date'] = nepali_str_to_english(end_date_nep_str)
        except Exception:
            self.add_error('end_date', "Invalid Nepali date format or non-existent date.")
        
        return cleaned_data

    