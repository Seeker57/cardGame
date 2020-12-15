from django import forms

class AuthForm(forms.Form):
    email = forms.EmailField(label='Почта')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')


class RegForm(forms.Form):
    login = forms.CharField(label='Ник')
    email = forms.EmailField(label='Почта')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    passwordConfirm = forms.CharField(widget=forms.PasswordInput(), label='Подтвердите пароль')


class CreateDeck(forms.Form):
    name = forms.CharField(label='Название колоды')
    hero = forms.CharField(label='Имя героя')


class EditDeck(forms.Form):
    deckID = forms.IntegerField(label='ID колоды')


class AddCard(forms.Form):
    cardID = forms.IntegerField(label='ID карты')