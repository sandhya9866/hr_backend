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
                'data-placeholder': 'Select Department Head(s)',
                'multiple': 'multiple'
            })
        } 