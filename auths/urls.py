from django.urls import path

from . import views

urlpatterns = [
    path('get-request-token', views.request_token, name='request_token'),
]