from django import forms
from .models import Shift

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ('title', 'colour', 'start_time', 'end_time', 'min_start_time', 'max_end_time')
        widgets = {
            'colour': forms.TextInput(attrs={'placeholder': 'Eg:Red/Blue/Green'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'min_start_time': forms.TimeInput(attrs={'type': 'time'}),
            'max_end_time': forms.TimeInput(attrs={'type': 'time'}),
        }   