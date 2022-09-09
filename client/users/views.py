from django.shortcuts import render,redirect
import httpx
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as user_logout
from django.contrib import messages

def login (request):
    next_path = request.GET.get('next' , '/')
    redirect_url = request.build_absolute_uri(next_path)
    res = httpx.get(f"http://127.0.0.1:8001/get-request-token/?redirect={redirect_url}").json()
    request_token = res['request_token']
    return redirect(f"http://127.0.0.1:8001/get_auth_token/?request_token={request_token}")

@login_required
def profile(request):
    return render(request , 'users/profile.html')

def home_page(request):
    return render(request , 'users/home.html')
    
def logout(request):
    user_logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect(f"http://127.0.0.1:8001/logout/?next={request.build_absolute_uri('/')}")