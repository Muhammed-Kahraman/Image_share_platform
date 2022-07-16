from django.db import models
from django import forms


# Create your models here.
class LoginFrom(forms.Form):
    username = forms.CharField(max_length=25, min_length=5, label="username")
    password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=5, label="Username")
    password = forms.CharField(max_length=20, min_length=5, label="Password", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, min_length=5, label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords doesn't match!")

        values = {
            "username": username,
            "password": password
        }

        return values


class ResetPasswordForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=5, label="Username")
    old_password = forms.CharField(max_length=20, min_length=5, label="Old Password", widget=forms.PasswordInput)
    password = forms.CharField(max_length=20, min_length=5, label="Password", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, min_length=5, label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        old_password = self.cleaned_data.get("old_password")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords doesn't match!")
        if len(password) < 8:
            raise forms.ValidationError("Password can't be smaller than 8 characters!")
        values = {
            "username": username,
            "old_password": old_password,
            "password": password
        }

        return values
