from django import forms
from .models import User, CloudAccount

class UserAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
        'password': forms.PasswordInput(),
    }


class CloudAccountAddForm(forms.ModelForm):
    class Meta:
        model = CloudAccount
        fields = '__all__'
        widgets = {
        'password': forms.PasswordInput(),
    }
