import json
import random
from collections import Counter
from .forms import *
from .models import *
from .function import *
from pathlib import Path
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.views.generic import TemplateView, ListView, CreateView

# Create your views here.


BASE_DIR = Path(__file__).resolve().parent.parent


def home(request):
    data = {}
    # data = loadMenu(request)
    return render(request, 'webGym/index.html', data)


class AboutView(ListView):
    template_name = "webGym/index.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = "kirill"
        return context

    def get_queryset(self):
        return 1


# class registration(ListView):
#     template_name = "webGym/reg.html"
#     context_object_name = 'posts'
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu'] = "kirill"
#         return context
#     def get_queryset(self):
#         return 1

# class auth(ListView):
#     template_name = "webGym/auth.html"
#     context_object_name = 'posts'
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu'] = "kirill"
#         return context
#     def get_queryset(self):
#         return 1

def Profile(request):
    data = {}
    data = loadMenu(request)
    return render(request, 'webGym/profile.html', data)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'webGym/reg.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = "kirill"
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'webGym/auth.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = "kirill"
        return context

    def get_success_url(self):
        return reverse_lazy('home')


@login_required
def my_cabinet(request):
    """Личный кабинет посетителя: статистика по абонементу и привязка карты."""
    user = request.user

    # Привязка карты по коду
    if request.method == 'POST':
        code = request.POST.get('card_code', '').strip()
        code = ''.join(ch for ch in code if ch.isdigit())
        if not code or len(code) != 10:
            messages.error(request, 'Введите 10-значный код карты.')
        else:
            ab = Abonement.objects.filter(card_code=code).select_related('user').first()
            if not ab:
                messages.error(request, 'Абонемент с таким кодом не найден.')
            elif ab.user_id != user.id and ab.user.username != user.username:
                # код уже занят другим пользователем — откажем в целях безопасности
                messages.error(request, 'Этот код уже привязан к другому аккаунту.')
            else:
                if ab.user_id != user.id:
                    ab.user = user
                    ab.save(update_fields=['user'])
                messages.success(request, 'Карта привязана!')
                return redirect('my')
        return redirect('my')

    # Актуальный абонемент (последний по времени)
    abonement = (Abonement.objects
                 .filter(user=user)
                 .order_by('-id')
                 .first())

    context = {'abonement': abonement, 'title': 'Личный кабинет'}

    if abonement:
        visits = list(Visit.objects.filter(user=user).order_by('-entered_at'))
        total_visits = len(visits)
        today = timezone.localdate()

        # Сколько осталось
        if abonement.abo_type == Abonement.TYPE_VISITS:
            remaining = abonement.remaining_visits
            remaining_text = f'{remaining} из {abonement.max_visits}'
        else:
            remaining = None
            if abonement.end_date:
                days_left = (abonement.end_date - today).days
                remaining_text = f'{days_left} дн. до конца' if days_left >= 0 else 'истёк'
            else:
                remaining_text = 'безлимит'

        # Посещения по месяцам / по дням за последние 30 дней
        days_counter = Counter(v.entered_at.date() for v in visits
                               if (today - v.entered_at.date()).days <= 29)
        by_day = [{'day': d.strftime('%d.%m'), 'n': days_counter[d]}
                  for d in sorted(days_counter)]

        # Посещения по времени (часы) — во сколько обычно приходит
        hours_counter = Counter(v.entered_at.hour for v in visits)
        by_hour = [{'hour': h, 'n': hours_counter.get(h, 0)} for h in range(24)]

        recent = visits[:12]

        context.update({
            'total_visits': total_visits,
            'remaining_text': remaining_text,
            'by_day': by_day,
            'by_hour': by_hour,
            'recent': recent,
            'status': abonement.status_text,
            'is_active': abonement.is_active,
        })

    return render(request, 'webGym/my.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def api(request):
    print(request.method)
    json_str = request.body.decode()
    data = json.loads(json_str)
    print(data['Name'])
    print(data['age'])
    return JsonResponse({"name": data['Name'], "age": data['age']})
