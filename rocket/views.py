from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate,update_session_auth_hash
from django.template import RequestContext
from rocket.forms import EditProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.views.generic import TemplateView
from django.contrib.auth.hashers import check_password
from .models import (
    Postform,
    Portal,
    Userprofile,
    user_activation_cache,
)
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.db import IntegrityError
from rocket import (
    forms,
    models,
    utils,
)


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

        #print form.is_valid()
        #print form.errors
        if form.is_valid():
            entrynum = utils.checkmail(form.cleaned_data['email'])
            if not entrynum:
                return HttpResponse("You should use a university's email ID")
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            try:
                Userprofile.objects.create(user = user, bio = form.cleaned_data['bio'], entryno = entrynum)
            except IntegrityError:
                raise
                #return HttpResponseRedirect('/signup')
            utils.send_confirm_email(user)

        else:
            return HttpResponseRedirect('/signup')

class activationview(TemplateView):

    def get(self, request, rhash):
        url_hash = rhash
        try:
            user_activate = user_activation_cache.objects.get(unique_hash = url_hash)
        except Exception as e:
            return HttpResponse('There is problem %s' % e)
        user_activate.user.is_active = True
        user_activate.user.save()
        user_activate.save()
        user_activation_cache.objects.filter(unique_hash = url_hash).delete()
        return HttpResponse('Activated sucessfully %s'%url_hash)

class loginview(TemplateView):

	template = 'rocket/login.html'
	form = forms.loginform

	def get(self, request):
		return render(request, self.template, {'form' : self.form()})

	def post(self, request):
		form = self.form(request.POST)
		#print form.is_valid()
		#print form.errors
		if form.is_valid():
			uname = form.cleaned_data['username']
			passw = form.cleaned_data['password']
			userq = models.Userprofile.objects.filter(user__username = uname)
			user = userq.first()
			if not user:
				return HttpResponse('No such user found')
			#print user.user.is_active
			if not user.user.is_active:
				return HttpResponse('User not activated')
			#print user.user.password
			if check_password(passw, user.user.password):
				return HttpResponse('Correct password')
			else:
				return HttpResponse('Incorrect password')
		else:
			return HttpResponseRedirect('/login')


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
























