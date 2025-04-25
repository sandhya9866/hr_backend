from django import forms
from django.forms import CharField

class UserLoginForm(forms.Form):

    username = CharField(max_length=255, required=True)
    password = CharField(max_length=255, required=True, widget=forms.PasswordInput)
    class Meta:
        fields = ['username', 'password']