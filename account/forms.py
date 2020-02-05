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
            raise forms.ValidationError('Please use your school email address')
        return cd['email']


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False,  widget=forms.Textarea(
                                  attrs={'placeholder': 'Short description about yourself'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cyber Security Science'}))
    interests = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'football, programming, computer-graphics, ...'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '07036653300'}))
    profile_photo = forms.ImageField(label='', widget=forms.ClearableFileInput(attrs={'hidden': '',
                                                                              'onchange': "loadProfileImg(event);",
                                                                              'accept': 'image/gif, image/jpeg, image/jpg, image/png'}))

    class Meta:
        model = Profile
        fields = ['profile_photo', 'gender', 'bio', 'department', 'interests',
                  'phone_number', 'year_of_entrance',
                  'year_of_graduation', 'allow_messages']
