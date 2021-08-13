from django import forms
from django.forms import ModelForm, Textarea, TextInput, ClearableFileInput, MultipleChoiceField, \
    CheckboxSelectMultiple, Select, CheckboxInput, SelectMultiple
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        error_messages = {
            'password1': {
                'required': _("this field is required."),
                'invalid': _("chose a valid password"),
                'validator': _("chose a valid password"),
            },
            'password2': {
                'required': _("this field is required."),
                'invalid': _("chose a valid password"),
                'validator': _("passwords don't match"),
            },
            'username': {
                'required': _("country field required."),
                'invalid': _("username should be less than 10 characters"),
                'validator': _("username should be less than 10 characters"),
            },
            'email': {
                'required': _("email field is required."),
                'invalid': _("please put a valid email address"),
                'validator': _("please put a valid email address"),
            },
        }


class AuthorProfileForm(ModelForm):
    class Meta:
        model = Author
        field = '__all__'
        exclude = ['user', 'uid', 'date_registered']
        error_messages = {
            'profile_pic': {
                'invalid': _("put a valid image file"),
            },
            # 'phone_no': {
            #     'invalid': _("put in a valid phone number"),
            # },

        }
        widgets = {
            'title': Select(attrs={
                'class': 'form-control',
            }),
            'gender': SelectMultiple(attrs={
                'class': 'form-control',
            }),
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        field = '__all__'
        exclude = ['author', 'post_id', 'date_added']

        widgets = {
            'body': Textarea(attrs={
                'class': 'form-control',
            }),
            'lead': CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'categories': SelectMultiple(attrs={
                'class': 'form-control',
            }),

        }


class PostCatForm(ModelForm):
    class Meta:
        model = PostCategory
        field = '__all__'
        exclude = []


class PostImageForm(ModelForm):
    class Meta:
        model = PostImage
        field = '__all__'
        exclude = ['date_added']


class SlideForm(ModelForm):
    class Meta:
        model = Slide
        field = '__all__'
        exclude = ['']


class FirstnameChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name']


class SurnameChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ['last_name']


class TitleChangeForm(ModelForm):
    class Meta:
        model = Author
        fields = ['title']
        widgets = {
            'title': Select(attrs={
                'class': 'form-control',
            }),

        }

