from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={ "class":"input-field", "placeholder": "Enter firstname"} ))
    last_name = forms.CharField(widget=forms.TextInput(attrs={ "class":"input-field", "placeholder": "Enter lastname"} ))
    username = forms.CharField(widget=forms.TextInput(attrs={ "class":"input-field", "placeholder": "Enter username"} ))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"input-field","placeholder": "Enter email"}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={"class":"input-field","placeholder": "Enter phone no"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input-field","placeholder": "Enter password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input-field","placeholder": "Confirm password"}))


    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email','phone_no']