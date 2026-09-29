from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Subscription


class LoginForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': "Неверный логин или пароль. Проверьте раскладку клавиатуры.",
    }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email (для напоминаний о списаниях)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['title', 'category', 'price', 'billing_date', 'is_active']
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
        }
