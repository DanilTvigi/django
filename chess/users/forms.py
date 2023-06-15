from django import forms
# from django.contrib.auth.models import CustomUser
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    # email = forms.CharField(label='Почтовый адрес')                      
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2'] #'email',


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser


