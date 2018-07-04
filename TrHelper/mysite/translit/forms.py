from django import forms
from .models import UserDict

class InputForm(forms.Form):

    kurd_input = forms.CharField(
        label='Paste kurdish names here',
        # initial='Paste kurdish names here',
        widget=forms.Textarea,
        max_length=100
        )

    ru_output = forms.CharField(
        required=False,
        initial='Here will be russian transliteration',
        help_text='Here will be russian transliteration',
        widget=forms.Textarea,
        max_length=100
        )

    info = forms.CharField(
        required=False,
        widget=forms.Textarea,
        disabled = True
        )

class AddForm(forms.ModelForm):
    class Meta:
        model = UserDict
        fields = ['kurd', 'ru', 'info']
