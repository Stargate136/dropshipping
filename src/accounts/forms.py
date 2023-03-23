from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from . import models

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  'email']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")

    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "email",
                  "password"]

class AddressForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")
    class Meta:
        model = models.ShippingAddress
        fields = ["alias",
                  "name",
                  "address_1",
                  "address_2",
                  "city",
                  "zip_code",
                  "country",
                  "email",
                  "password"]
