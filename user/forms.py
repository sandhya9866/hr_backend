from django import forms
from .models import Profile
from .models import AuthUser

class UserForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('dob', 'gender', 'marital_status', 'address', 'mobile_number', 'personal_email', 'religion', 'blood_group', 'shift')
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }