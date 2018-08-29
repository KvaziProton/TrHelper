from django import forms
from django.forms import ModelChoiceField

from .models import User, CloudAccount, Article

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

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.translator:
            return '{} переводится'.format(obj.title)
        return obj.title


class AddArticleForm(forms.Form):
    url = forms.URLField()
    translated_title = forms.CharField()
    article_select = MyModelChoiceField(
        queryset=Article.objects.exclude(language='english'),
        required=False
        )
        #will return pk 

    def clean_url(self):
        data = self.cleaned_data['url']
        if 'anfkurdi' not in data:
            raise forms.ValidationError("You should paste url from kurdish anfnews!")
        return data
