from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'department_head']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department_head': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Select Department Head',
                'multiple': 'multiple'
            })
        } 

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Override the label_from_instance to show full name
    #     self.fields['department_head'].label_from_instance = lambda obj: obj.full_name() 