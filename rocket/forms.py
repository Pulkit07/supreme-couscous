from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from rocket.models import Userprofile
from django.core.files.images import get_image_dimensions


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    email = forms.EmailField(max_length=250)
    bio = forms.CharField(max_length=500, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )


class loginform(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(widget=forms.PasswordInput())


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'password',
        }


class UplaodImageForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Userprofile
        fields = ('image',)

    def clean_avatar(self):
        image = self.cleaned_data['image']

        try:
            w, h = get_image_dimensions(image)

            # validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub in [
                    'jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # validate file size
            if len(image) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return image
