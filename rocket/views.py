from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.template import RequestContext
from rocket.forms import EditProfileForm, UplaodImageForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
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


class home(TemplateView):

    template = 'rocket/home.html'

    def get(self, request):
        return render(request, self.template)


class grievances(TemplateView):
    template_name = "grievances/grievances.html"

    def get(self, request):
        form = Postform(initial={"user": request.user})
        post = Portal.objects.all()
        args = {"form": form, "posts": post}
        return render(request, self.template_name, args)

    def post(self, request):
        name = request.user
        form = Postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = name
            post.save()
            return redirect('/account/grievances/')
        posts = Portal.objects.all()
        form = Postform()
        args = {"posts": posts, "form": form}
        return render(request, self.template_name, args)


class signup(TemplateView):

    template = 'rocket/signup.html'

    def get(self, request):
        useractive = session_has_user(request)
        if useractive:
            return HttpResponse("This user is already logged in: %s" % useractive)
        form = forms.SignUpForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = forms.SignUpForm(request.POST)

        # print form.is_valid()
        # print form.errors
        if form.is_valid():
            entrynum = utils.checkmail(form.cleaned_data['email'])
            if not entrynum:
                return HttpResponse("You should use a university's email ID")
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            try:
                Userprofile.objects.create(
                    user=user, bio=form.cleaned_data['bio'], entryno=entrynum)
            except IntegrityError:
                raise
                # return HttpResponseRedirect('/signup')
            utils.send_confirm_email(user)

        else:
            return HttpResponseRedirect('/signup')


class activationview(TemplateView):

    def get(self, request, rhash):
        url_hash = rhash
        try:
            user_activate = user_activation_cache.objects.get(
                unique_hash=url_hash)
        except Exception as e:
            return HttpResponse('There is problem %s' % e)
        user_activate.user.is_active = True
        user_activate.user.save()
        user_activate.save()
        user_activation_cache.objects.filter(unique_hash=url_hash).delete()
        return HttpResponse('Activated sucessfully %s' % url_hash)


class logoutview(TemplateView):

    def get(self, request):
        useractive = session_remove_user(request)
        return HttpResponse("This user has been successfully logged out: %s" % useractive)


class loginview(TemplateView):

    template = 'rocket/login.html'
    form = forms.loginform

    def get(self, request):
        useractive = session_has_user(request)
        if useractive:
            return HttpResponse("This user is already logged in: %s" % useractive)
        return render(request, self.template, {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST)
        # print form.is_valid()
        # print form.errors
        if form.is_valid():
            uname = form.cleaned_data['username']
            passw = form.cleaned_data['password']
            userq = models.Userprofile.objects.filter(user__username=uname)
            user = userq.first()
            if not user:
                return HttpResponse('No such user found')
            else:
                if not check_password(passw, user.user.password):
                    return HttpResponse("Incorrect Password")
                else:
                    if not user.user.is_active:
                        return HttpResponse('User not activated')
                    session_add_user(uname)
                    return HttpResponse('Login Successful')
        else:
            return HttpResponseRedirect('/login')


class profilepageview(TemplateView):
    '''This view is a generic view to load the profile of any user which exists in the database.'''

    template = 'rocket/profilepage.html'

    def get(self, request, uname):
        activeuser = session_has_user(request)
        if not activeuser:
            return HttpResponse("You need to login before viewing anyone's profile")
        userq = models.Userprofile.objects.filter(user__username=uname)
        user = userq.first()
        if not user:
            return HttpResponse('No such user found')
        else:
            args = {'user': user}
            return render(request, self.template, args)


class Profile(TemplateView):
    template_name = 'rocket/profile.html'

    def get(self, request):
        activeuser = session_has_user(request)
        if not activeuser:
            return HttpResponse("Unable to show profile, no user logged in")
        profile = Userprofile.objects.filter(user=activeuser)
        details = profile[0]
        pic = details.image
        args = {'user': request.user, 'details': details, 'pic': pic}
        return render(request, 'rocket/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'rocket/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile')
        else:
            return redirect('rocket/change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'rocket/change_password.html', args)


class ImageUpload(TemplateView):
    template_name = 'rocket/upload_profile_picture.html'

    def get(self, request):
        profiles = Userprofile.objects.get(user=request.user)
        pic = profiles.image
        form = UplaodImageForm(initial={'image': profiles.image})
        args = {'form': form, 'user': request.user, 'pic': pic}
        return render(request, self.template_name, args)

    def post(self, request):
        name = request.user
        details = Userprofile.objects.get(user=name)
        primerykey = details.pk
        form = UplaodImageForm(request.POST, request.FILES)
        if form.is_valid():
            Userprofile.objects.filter(user=name).delete()
            profile = form.save(commit=False)
            profile.user = request.user
            profile.bio = details.bio
            profile.enrtyno = details.entryno
            profile.phone = details.phone
            profile.pk = primerykey
            profile.image = request.FILES['image']
            profile.save()
            return redirect('/profile')
        # pic=form.cleaned_data['image']
        args = {'user': request.user, 'form': form}
        return render(request, 'rocket/profile.html', args)


# Some utility functions related to dealing with request.session

def session_has_user(request):
    '''Checks whether the session has an entry of username logged in'''
    return request.session.get('username')


def session_add_user(request, username):
    '''Adds a user to the sesssion'''
    if session_has_user(request):
        return False
    request.session['username'] = username
    return True


def session_remove_user(request):
    '''Removes the user from the session '''
    try:
        return request.session.pop('username')
    except KeyError:
        return False
