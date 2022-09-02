from django.urls import path

from . import views

urlpatterns = [
    path('get-request-token/', views.request_token, name='request_token'),
    path('login/' , views.login , name='login'),
    path('check_auth_token/' , views.check_auth_token , name='check_auth_token')
]