from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate,update_session_auth_hash
from django.template import RequestContext
from rocket.forms import SignUpForm,EditProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.views.generic import TemplateView
from .models import Postform,Portal


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

def signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            subject='Thankyou for  signup'
            message='welcome to our world'
            from_email=settings.EMAIL_HOST_USER
            to_list=[save_it.email,settings.EMAIL_HOST_USER]
            send_mail(subject,messages,from_email,to_list,fail_silently=True)

            messages.success('thankyou')
            return HttpResponseRedirect('/rocket/')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    
        args={'form':form}
        return render(request,'rocket/signup.html',args)

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
























