from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate,update_session_auth_hash
from django.template import RequestContext
from rocket.forms import EditProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.views.generic import TemplateView
from .models import Postform, Portal, Userprofile
from django.http import HttpResponse
from rocket import forms


def home(request):
    args={'message': 'message'}
    return render(request,'rocket/home.html', args)


class grievances(TemplateView):
    template_name = "grievances/grievances.html"
    def get(self,request):
        form=Postform(initial={"user":request.user})
        post=Portal.objects.all()
        args={"form":form,"posts":post}
        return render(request,self.template_name,args)
    def post(self,request):
        name=request.user
        form=Postform(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=name
            post.save()
            return redirect('/account/grievances/')
        posts=Portal.objects.all()
        form=Postform()
        args={"posts":posts,"form":form}
        return render(request,self.template_name,args)


class signup(TemplateView):

    template = 'rocket/signup.html'

    def get(self, request):
        form = forms.SignUpForm()
        return render(request, self.template, {'form' : form})

    def post(self, request):
        form = forms.SignUpForm(request.POST)

        if form.is_valid():
            entrynum = utils.checkmail(form.cleaned_data['email'])
            if not entrynum:
                return HttpResponse("You should use a university's email ID")
            user = form.save()
            Userprofile.objects.create(user = user, bio = form.cleaned_data['bio'], entryno = entryno)
            utils.send_confirm_email(form.cleaned_data['first_name'],
                        form.cleaned_data['last_name'], form.cleaned_data['email'])

        else:
            return redirect(request, self.template, {'form' : forms.SignUpForm()})


def profile(request):
    args = {'user':request.user}
    return render(request,'rocket/profile.html',args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/rocket/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = { 'form': form}
        return render(request, 'rocket/edit_profile.html',args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/rocket/profile')
        else:
            return redirect('rocket/change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'rocket/change_password.html',args)
























