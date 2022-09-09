from contextlib import redirect_stderr
from multiprocessing import context
from django.shortcuts import render , redirect
from .models import Authentication, my_function
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.urls import reverse
from django.contrib.auth import logout as user_logout
from django.contrib import messages


# Create your views here.
def request_token(request):
    
    redirect = request.GET['redirect']
    record = Authentication.objects.create(redirect_url = redirect)
    return JsonResponse({'request_token' : record.request_token})

def login(request):
    if(request.method == 'POST'):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            user_login(request , user)
            return redirect(reverse('get_auth_token') + '?request_token=' + request.GET['request_token'])
    
    else:
        form = AuthenticationForm()    
    
    context = {
        'form' : form,
        'title' : 'login page'
    }
    return render(request , 'auths/login.html' , context=context)

@login_required
def get_auth_token(request):
    request_token = request.GET['request_token']
    record = Authentication.objects.get(request_token = request_token)
    record.auth_token = my_function()
    record.user = request.user
    record.save()
    return redirect(record.redirect_url + '?auth_token=' + record.auth_token)
    
def check_auth_token(request):
    try:
        auth_token = request.GET['auth_token']
        record = Authentication.objects.get(auth_token = auth_token)
        user = record.user
        my_user = {
            'user_id' : user.id,
            'username' : user.username,
            'email' : user.email
        }
        record.delete()
        return JsonResponse({'user' : my_user})
    except:
        return JsonResponse({'status':'false','message': '403 Forbidden'}, status=403)

def register(request) :
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            user_login(request , user)
            return redirect(reverse('get_auth_token') + '?request_token=' + request.GET['request_token'])
    else:
        form = UserCreationForm()
    context = {
        'form' : form,
        'title' : 'registration page'
    }      
    return render(request , 'auths/register.html' , context)  

def logout(request):
    user_logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect(request.GET('next'))
