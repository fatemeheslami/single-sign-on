from urllib import response
import httpx
from django.contrib.auth.models import User
from django.contrib.auth import login

class CheckAuthTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        auth_token = request.GET.get('auth_token' , None)
        if auth_token:
            user = self.check_auth_token(auth_token)
            if user:
                login(request , user)

        response = self.get_response(request)
        return response
    
    def check_auth_token(self , auth_token):
        res = httpx.get(f"http://127.0.0.1:8001/check_auth_token/?auth_token={auth_token}")
        if res.status_code != 403:
            return self.build_user(res.json().get('user'))
        return None
    
    def build_user(self , json_user):
        try:
            user = User.objects.get(username = json_user['username'])
            user.email = json_user['email']
        except User.DoesNotExist:
            user = User(username = json_user['username'] , email = json_user['email'])
        
        user.set_unusable_password()
        user.save()
        return user