from django import forms
from payroll.models import SalaryType

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