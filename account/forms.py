from django import forms
from django.contrib.auth.models import User
from taggit_selectize import widgets as tag_widget

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'placeholder': 'First Name    Last Name'}))
    last_name = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'interests': tag_widget.TagSelectize(),
        }

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

    def save(self, commit=True):
        instance = super(UserRegistrationForm, self).save(commit=False)
        _name = self.cleaned_data.get('first_name').split(' ')
        instance.first_name = _name[0]
        instance.last_name = ' '.join(_name[1:])
        instance.save()
        return instance


class StudentProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False,  widget=forms.Textarea(
                                  attrs={'placeholder': 'Short description about yourself'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cyber Security Science'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '07036653300'}))
    profile_photo = forms.ImageField(required=False, label='',
                                     widget=forms.ClearableFileInput(attrs={'hidden': '',
                                                                            'onchange': "loadProfileImg(event);",
                                                                            'accept': 'image/gif, image/jpeg,'
                                                                                      ' image/jpg, image/png'}))

    class Meta:
        model = Profile
        fields = ['profile_photo', 'gender', 'bio',
                  'department', 'interests',
                  'phone_number', 'year_of_entrance',
                  'year_of_graduation']
        widgets = {
            'interests': tag_widget.TagSelectize(),
        }

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['interests'].widget.attrs['placeholder'] = 'football, photography, programming'


class StaffProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False,
                          widget=forms.Textarea(attrs={'placeholder': 'Short description about yourself'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cyber Security Science'}))
    phone_number = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'placeholder': '07036653300'}))
    profile_photo = forms.ImageField(required=False, label='',
                                     widget=forms.ClearableFileInput(attrs={'hidden': '',
                                                                            'onchange': "loadProfileImg(event);",
                                                                            'accept': 'image/gif, image/jpeg,'
                                                                                      ' image/jpg, image/png'}))

    class Meta:
        model = Profile
        fields = ['profile_photo', 'gender', 'bio',
                  'department', 'interests',
                  'phone_number', 'staff_status', ]
        widgets = {
            'interests': tag_widget.TagSelectize(),
        }

    def __init__(self, *args, **kwargs):
        super(StaffProfileForm, self).__init__(*args, **kwargs)
        self.fields['interests'].widget.attrs['placeholder'] = 'football, photography, programming'


class EditStaffProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False,
                          widget=forms.Textarea(attrs={'placeholder': 'Short description about yourself'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cyber Security Science'}))
    phone_number = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'placeholder': '07036653300'}))
    profile_photo = forms.ImageField(required=False, label='',
                                     widget=forms.ClearableFileInput(attrs={'hidden': '',
                                                                            'onchange': "loadProfileImg(event);",
                                                                            'accept': 'image/gif, image/jpeg,'
                                                                                      ' image/jpg, image/png'}))

    class Meta:
        model = Profile
        fields = ['profile_photo', 'gender', 'bio',
                  'department', 'interests',
                  'phone_number', 'staff_status', ]
        widgets = {
            'interests': tag_widget.TagSelectize(),
        }

    def __init__(self, *args, **kwargs):
        super(EditStaffProfileForm, self).__init__(*args, **kwargs)
        self.fields['interests'].widget.attrs['placeholder'] = 'football, photography, programming'


class EditProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False,
                          widget=forms.Textarea(
                                  attrs={'placeholder': 'Short description about yourself'}))
    department = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Cyber Security Science'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '07036653300'}))
    profile_photo = forms.ImageField(label='',
                                     widget=forms.ClearableFileInput(attrs={'hidden': True,
                                                                            'onchange': "loadProfileImg(event);",
                                                                            'accept': 'image/gif, image/jpeg,'
                                                                                      'image/jpg, image/png'}))

    class Meta:
        model = Profile
        fields = ['profile_photo', 'gender',
                  'bio', 'department', 'interests',
                  'phone_number', 'year_of_graduation']
        widgets = {
            'interests': tag_widget.TagSelectize(),
        }

