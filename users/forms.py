from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm


# class UserSignUpForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     permission = forms.ChoiceField(choices=UserProfile.PERMISSION_CHOICES)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']


# class UserSignInForm(forms.Form):
#     username = forms.CharField(max_length=255)
#     password = forms.CharField(widget=forms.PasswordInput)



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    permission = forms.ChoiceField(
        choices=UserProfile.PERMISSION_CHOICES,
        widget=forms.Select(
            attrs={
                "placeholder": "Permission",
                "class": "form-control"
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))

    organization = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

