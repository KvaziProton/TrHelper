# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User, Translator, LANGUAGE_CHOICES
#
#
# class TranslatorSignUpForm(UserCreationForm):
#     languages = forms.MultipleChoiceField(choices=LANGUAGE_CHOICES)
#
#     class Meta(UserCreationForm.Meta):
#         model = User
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_translator = True
#         if commit:
#             user.save()
#         return user
#
#
# class EditorSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username', 'password1', 'password2',)
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_editor = True
#         if commit:
#             user.save()
#         return user
