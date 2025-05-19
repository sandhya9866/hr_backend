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
        fields = ('dob', 'gender', 'marital_status', 'address', 'mobile_number', 'personal_email', 'religion', 'blood_group', 'shift', 'job_type', 'joining_date')
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD (BS)', 'id': 'joining_date'}),

        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['gender'].choices = [
            choice for choice in self.fields['gender'].choices if choice[0] != 'A'
        ]

        self.fields['marital_status'].choices = [
            choice for choice in self.fields['marital_status'].choices if choice[0] != 'A'
        ]

        self.fields['religion'].choices = [
            choice for choice in self.fields['religion'].choices if choice[0] != 'A'
        ]

        self.fields['job_type'].choices = [
            choice for choice in self.fields['job_type'].choices if choice[0] != 'all'
        ]