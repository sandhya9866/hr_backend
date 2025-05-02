from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('type', 'date', 'time', 'reason')
        widgets = {
            'type': forms.Select(choices=[('missed_checkout', 'Missed Checkout'), ('late_arrival_request', 'Late Arrival Request'), ('early_departure_request', 'Early Departure Request')]),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'placeholder': 'Write reason here...'}),
        }   