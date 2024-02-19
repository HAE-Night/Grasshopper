from django.contrib import auth
from django import forms
from django.contrib.auth import authenticate

from .models import Products
from django.contrib.auth.forms import AuthenticationForm


class ImageForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['ITEM_PHOTO']


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "input"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "input"
            }
        ))
