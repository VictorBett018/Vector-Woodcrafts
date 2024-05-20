from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={ "class":"input-field"} ))
    last_name = forms.CharField(widget=forms.TextInput(attrs={ "class":"input-field"} ))
    username = forms.CharField(widget=forms.TextInput(attrs={ "class":"input-field"} ))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"input-field"}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={"class":"input-field"}))
    address = forms.CharField(widget=forms.TextInput(attrs={ "class":"input-field"} ))
    city = forms.CharField(widget=forms.TextInput(attrs={ "class":"input-field"} ))
    company = forms.CharField(widget=forms.TextInput(attrs={ "class":"input-field"} ))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input-field"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input-field"}))



    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email','phone_no']