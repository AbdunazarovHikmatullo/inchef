from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=13)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone_number',
            'role',
            'password1',
            'password2',
        )

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not phone.startswith('+992'):
            raise forms.ValidationError("Номер должен начинаться с +992")
        return phone


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Неверный логин или пароль")

        cleaned_data['user'] = user
        return cleaned_data
