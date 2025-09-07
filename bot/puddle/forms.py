from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import URLValidator
from django.forms import formset_factory
from .models import CustomUser, Newsletter
from django import forms


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль',
    }))


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'telegram_api_id', 'telegram_api_hash', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя',
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Почта',
    }))

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Номер телефона',
            'type': 'tel'
        }),
        max_length=20,
        label='Телефон'
    )

    telegram_api_id = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'api_id',
    }))

    telegram_api_hash = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'api_hash',
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль',
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Повторите пароль',
    }))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        user.telegram_api_id = self.cleaned_data['telegram_api_id']
        user.telegram_api_hash = self.cleaned_data['telegram_api_hash']
        if commit:
            user.save()
        return user


class TelegramAuthForm(forms.Form):
    session_name = forms.CharField(
        label='Название сессии',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class Telegram2FAForm(forms.Form):
    verification_code = forms.CharField(
        label='Код подтверждения из Telegram',
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXXXX'
        })
    )
    password = forms.CharField(
        label='Пароль 2FA (если установлен)',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class ChatLinkForm(forms.Form):
    link = forms.URLField(
        label='Ссылка на чат',
        widget=forms.URLInput(attrs={
            'placeholder': 'https://t.me/chatname'
        }),
        validators=[URLValidator()]
    )


ChatLinkFormSet = formset_factory(ChatLinkForm, extra=1, max_num=10)


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['text', 'file', 'file2', 'file3', 'file3', 'file4', 'file5']


class RemoveChatForm(forms.Form):
    chat_url = forms.CharField(widget=forms.HiddenInput())