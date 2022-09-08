from django.urls import path

from . import views
urlpatterns = [
    path('login/' , views.login , name='login'),
    path('index/' , views.index , name='index'),
    path('logout/' , views.logout , name='logout'),
    path('' , views.home_page , name='home_page')
]