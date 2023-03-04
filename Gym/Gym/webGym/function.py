from django.shortcuts import render
from .models import *


#Загрузка меню
def loadMenu(request):
    data = {}
    data['icon'] = main_icon.objects.all().order_by('Position')  # Ищем все пункты и сортируем по позиции
    data['Menu'] = MainMenu.objects.all().order_by('Position') #Ищем все пункты и сортируем по позиции
    data['banner'] = banner.objects.all().order_by('Position')  # Ищем все пункты и сортируем по позиции
    data['banner_button'] = banner_button.objects.all().order_by('Position')  # Ищем все пункты и сортируем по позиции
    data['active_tab'] = request.resolver_match.view_name #В зависимости от текущей страницы назначем активную в меню

    return data