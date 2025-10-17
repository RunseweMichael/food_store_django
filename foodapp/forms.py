from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationForm(forms.Form):
    firstName = forms.CharField(max_length=255)
    lastName = forms.CharField(max_length=255)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField(required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
