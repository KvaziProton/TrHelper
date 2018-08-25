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


class EmbedArticleForm(forms.Form):
    url = forms.URLField()

    def clean_url(self):
        data = self.cleaned_data['url']
        if 'anf' not in data:
            raise forms.ValidationError("You should paste url from anfnews!")
        return data
