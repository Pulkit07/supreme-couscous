from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.template import RequestContext
from rocket.forms import SignUpForm

def home(request):
    args={'message': 'message'}
    return render(request,'rocket/home.html', args)
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
            return HttpResponseRedirect('/')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    
        args={'form':form}
        return render(request,'rocket/signup.html',args)
