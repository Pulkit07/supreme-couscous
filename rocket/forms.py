from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length = 40)
    last_name = forms.CharField(max_length = 40)
    email = forms.EmailField(max_length = 250)
    bio = forms.CharField(max_length = 500, required = False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class loginform(forms.Form):
	username = forms.CharField(max_length = 40)
	password = forms.CharField(widget = forms.PasswordInput())


class EditProfileForm(UserChangeForm):

    class Meta:
        model=User
        fields={
            'username',
            'first_name',
            'last_name',
            'password',
        }
