from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords don\'t match')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if 'futminna.edu.ng' not in cd['email']:
            raise forms.ValidationError('Please use an academic institution\'s email address')
        return cd['email']


class ProfileForm(forms.ModelForm):
    profile_photo = forms.ImageField(label='')

    class Meta:
        model = Profile
        fields = ['profile_photo', 'gender', 'bio', 'department', 'interests',
                  'phone_number', 'allow_messages', 'year_of_entrance',
                  'year_of_graduation']
