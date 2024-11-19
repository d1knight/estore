from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Введите надёжный пароль.",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Введите тот же пароль для подтверждения.",
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Логин',
        }
        help_texts = {
            'username': None,  # Убираем стандартные подсказки для логина
        }
