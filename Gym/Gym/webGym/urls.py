from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    path('', RedirectView.as_view(url='/home', permanent=False), name='home'),
    path('home/', views.home, name='home'),
    path('my/', MyCabinet.as_view(), name='my'),
    path('test/', AboutView.as_view()),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('auth/', LoginUser.as_view(), name='auth'),
    path('logout/', logout_user, name='logout'),
    path('api/info', views.api),

]


