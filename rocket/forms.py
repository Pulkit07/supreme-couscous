from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name=forms.CharField(max_length=40,required=False,help_text='optional')
    last_name=forms.CharField(max_length=40,required=False,help_text='optional')
    email=forms.EmailField(max_length=250,help_text='please inform a valid email address')

    class Meta:
        model=User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class EditProfileForm(UserChangeForm):

    class Meta:
        model=User
        fields={
            'username',
            'first_name',
            'last_name',
            'password',
        }
