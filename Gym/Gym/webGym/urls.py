from . import views
from .views import *
from .API.v1 import frontend
from django.urls import path
from django.views.generic.base import RedirectView
from . import gateviews


urlpatterns = [

    path('', RedirectView.as_view(url='/home', permanent=False), name='home'),
    path('home/', views.home, name='home'),
    path('my/', MyCabinet.as_view(), name='my'),
    path('profile/', Profile, name='profile'),
    path('test/', AboutView.as_view()),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('auth/', LoginUser.as_view(), name='auth'),
    path('logout/', logout_user, name='logout'),

    # ------------------- Проходная (оператор проходной) ---------------------
    path('gate/', gateviews.gate_panel, name='gate_panel'),
    path('gate/stats/', gateviews.gate_stats, name='gate_stats'),
    path('gate/abonements/', gateviews.gate_abonements, name='gate_abonements'),
    path('gate/abonements/<int:pk>/delete/', gateviews.gate_abonement_delete,
         name='gate_abonement_delete'),
    path('gate/trainers/', gateviews.trainer_list, name='trainer_list'),
    path('gate/trainers/add/', gateviews.trainer_add, name='trainer_add'),
    path('gate/trainers/<int:pk>/delete/', gateviews.trainer_delete, name='trainer_delete'),


    #-----------------------------------API---------------------------

    path('api/mycabinet', frontend.myCabinet),
    path('api/users/', frontend.UserList.as_view()),
    path('api/users//', frontend.UserDetail.as_view()),
    path('api/info', views.api),

]


