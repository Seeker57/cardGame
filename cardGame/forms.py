from django import forms

class AuthForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegForm(forms.Form):
    login = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    passwordConfirm = forms.CharField(widget=forms.PasswordInput())
