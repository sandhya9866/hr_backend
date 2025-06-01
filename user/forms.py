from django import forms
from .models import Profile, WorkingDetail
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
        fields = ('dob', 'gender', 'marital_status', 'address', 'mobile_number', 'personal_email', 'religion', 'blood_group')
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
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

        self.fields['mobile_number'].required = True

class WorkingDetailForm(forms.ModelForm):
    class Meta:
        model = WorkingDetail
        fields = ('shift', 'job_type', 'joining_date', 'department')
        widgets = {
            'joining_date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD (BS)', 'id': 'joining_date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job_type'].choices = [
            choice for choice in self.fields['job_type'].choices if choice[0] != 'all'
        ]
