from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class LoginForm(forms.Form):
    username=forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Enter email'}))
    password=forms.CharField(widget=forms.PasswordInput)
    
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    phone_number = forms.IntegerField(validators=[MinValueValidator(61000000), 
                    MaxValueValidator(65999999)])
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

from .models import Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields=('username',)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=('city', 'address', 'phone_number',)