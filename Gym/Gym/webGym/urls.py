from . import views
from .views import *
from .API.v1 import frontend
from django.urls import path
from django.views.generic.base import RedirectView


urlpatterns = [

    path('', RedirectView.as_view(url='/home', permanent=False), name='home'),
    path('home/', views.home, name='home'),
    path('my/', MyCabinet.as_view(), name='my'),
    path('test/', AboutView.as_view()),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('auth/', LoginUser.as_view(), name='auth'),
    path('logout/', logout_user, name='logout'),


    #-----------------------------------API---------------------------

    path('api/mycabinet', frontend.myCabinet),
    path('api/users/', frontend.UserList.as_view()),
    path('api/users//', frontend.UserDetail.as_view()),
    path('api/info', views.api),

]


