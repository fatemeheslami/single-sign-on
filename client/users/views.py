from django.shortcuts import render,redirect
import httpx
from django.contrib.auth.decorators import login_required

def login (request):
    next_path = request.GET.get('next' , '/')
    redirect_url = request.build_absolute_uri(next_path)
    res = httpx.get(f"http://127.0.0.1:8001/get-request-token/?redirect={redirect_url}").json()
    request_token = res['request_token']
    return redirect(f"http://127.0.0.1:8001/login/?request_token={request_token}")

@login_required
def profile(request):
    return render(request , 'users/profile.html')