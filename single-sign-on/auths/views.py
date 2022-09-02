from contextlib import redirect_stderr
from multiprocessing import context
from django.shortcuts import render , redirect
from .models import Authentication, my_function
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def request_token(request):
    
    redirect = request.GET['redirect']
    record = Authentication.objects.create(redirect_url = redirect)
    return JsonResponse({'request_token' : record.request_token})

def login(request):
    if(request.method == 'POST'):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            request_token = request.GET['request_token']
            record = Authentication.objects.get(request_token = request_token)
            record.auth_token = my_function()
            record.user = user
            record.save()
            return redirect(record.redirect_url + '?auth_token=' + record.auth_token)
    
    else:
        form = AuthenticationForm()    
    
    context = {
        'form' : form,
        'title' : 'login page'
    }
    return render(request , 'auths/login.html' , context=context)

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