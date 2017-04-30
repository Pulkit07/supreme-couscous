from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms


# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Userprofile(models.Model):
    user = models.ForeignKey(User)
    description = models.CharField(max_length=100,default='')
    city = models.CharField(max_length=100,default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile  = Userprofile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class Portal(models.Model):
    user=models.ForeignKey(User)
    Post=models.TextField(max_length=1000,default=" ",blank=False,)
    date_created=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

#form for taking grievance
class Postform(forms.ModelForm):
     Post = forms.CharField(required=False,widget=forms.Textarea(
                                  attrs={
                                      'class': 'form-control',
                                      'placeholder': 'Write a Description..'
                                  }
                                  ))
     class Meta:
        model=Portal
        fields= ('user','Post','date_created',)
