
from django import forms
from .models import ApprovedRegistrations

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = ApprovedRegistrations
        fields = ['first_name', 'last_name', 'phone_number', 'address1', 'city', 'state', 'image', 'signature', 'password', 'confirm_password']
