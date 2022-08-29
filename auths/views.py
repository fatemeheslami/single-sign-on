from django.shortcuts import render
from .models import Authentication
from django.http import JsonResponse

# Create your views here.
def request_token(request):
    
    redirect = request.GET['redirect']
    record = Authentication.objects.create(redirect_url = redirect)
    return JsonResponse({'request_token' : record.request_token})