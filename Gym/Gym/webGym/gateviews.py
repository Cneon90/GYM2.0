"""Модуль «Проходная» — интерфейс оператора проходной.

Роль: группа «Оператор проходной» + права can_manage_gate / can_manage_trainers.
"""
from collections import Counter
from datetime import timedelta

from django import forms
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import AbonementForm, TrainerUserForm
from .models import Abonement, Visit, Trainer


def gate_permission_required():
    return permission_required('webGym.can_manage_gate', raise_exception=True)


def role_for(request, role_name):
    """Проверяет принадлежность пользователя к группе-роли."""
    if not request.user.is_authenticated:
        return False
    return request.user.groups.filter(name=role_name).exists()


TRAINER_GROUP_NAME = 'Тренер'


def _trainer_group():
    return Group.objects.get_or_create(name=TRAINER_GROUP_NAME)[0]


# ---------------------------------------------------------------------------
# Панель проходной: поиск пользователя, проверка абонемента, отметка входа
# ---------------------------------------------------------------------------
@login_required
@gate_permission_required()
def gate_panel(request):
    found_user = None
    abonement = None
    if request.method == 'POST':
        # Отметка входа по кнопке
        uid = request.POST.get('checkin_user_id')
        if uid and request.user.has_perm('webGym.can_manage_gate'):
            user = User.objects.filter(id=uid).first()
            ab = Abonement.objects.filter(user=user).order_by('-id').first()
            if user and ab and ab.is_active:
                # защита от двойной отметки в течение 10 минут
                recent = Visit.objects.filter(
                    user=user,
                    entered_at__gte=timezone.now() - timedelta(minutes=10),
                ).first()
                if recent:
                    messages.warning(request,
                                     f'{user.username} уже отмечал вход в {recent.entered_at.strftime("%H:%M")}.')
                    return redirect('gate_panel')
                Visit.objects.create(user=user, abonement=ab, operator=request.user)
                messages.success(request, f'Вход отмечен: {user.username}.')
            else:
                messages.error(request, 'Вход запрещён: нет активного абонемента.')
            return redirect('gate_panel')

        # Поиск пользователя: по коду карты или по имени/логину
        query = request.POST.get('q', '').strip()
        if query:
            # быстрый скан карты: 10 цифр (позволяем пробелы/другие разделители)
            digits_query = ''.join(ch for ch in query if ch.isdigit())
            if len(digits_query) == 10:
                ab = (Abonement.objects
                      .filter(card_code=digits_query)
                      .select_related('user')
                      .order_by('-id')
                      .first())
                if ab:
                    found_user = ab.user
                    abonement = ab
                else:
                    found_user = None
            else:
                found_user = (User.objects
                              .filter(username__iexact=query)
                              .first())
                if not found_user:
                    found_user = (User.objects
                                  .filter(first_name__icontains=query)
                                  .filter(last_name__icontains=query)
                                  .first())
                if found_user:
                    abonement = (Abonement.objects
                                 .filter(user=found_user)
                                 .order_by('-id')
                                 .first())

    context = {
        'found_user': found_user,
        'abonement': abonement,
        'title': 'Проходная',
    }
    return render(request, 'webGym/gate_panel.html', context)


# ---------------------------------------------------------------------------
# Статистика посещений
# ---------------------------------------------------------------------------
@login_required
@gate_permission_required()
def gate_stats(request):
    today = timezone.localdate()
    week = today - timedelta(days=7)
    visits_today = Visit.objects.filter(entered_at__date=today).count()
    visits_week = Visit.objects.filter(entered_at__date__gte=week).count()
    total = Visit.objects.count()
    active_abos = Abonement.objects.count()

    recent_visits = list(Visit.objects.select_related('user', 'operator')[:15])

    from collections import Counter
    week_visits = Visit.objects.filter(entered_at__date__gte=week)
    day_counter = Counter(v.entered_at.date() for v in week_visits.only('entered_at'))
    by_day_list = [{'day': d.strftime('%d.%m'), 'n': day_counter[d]}
                   for d in sorted(day_counter)]

    context = {
        'visits_today': visits_today,
        'visits_week': visits_week,
        'total': total,
        'active_abos': active_abos,
        'recent_visits': recent_visits,
        'by_day': by_day_list,
        'title': 'Статистика посещений',
    }
    return render(request, 'webGym/gate_stats.html', context)


# ---------------------------------------------------------------------------
# Управление абонементами
# ---------------------------------------------------------------------------
@login_required
@gate_permission_required()
def gate_abonements(request):
    if request.method == 'POST':
        form = AbonementForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Абонемент сохранён.')
                return redirect('gate_abonements')
            except forms.ValidationError as e:
                messages.error(request, '; '.join(e.messages))
        else:
            messages.error(request, 'Проверьте данные формы.')
    else:
        form = AbonementForm()

    abonements = (Abonement.objects
                  .select_related('user')
                  .order_by('-id')[:50])
    context = {
        'form': form,
        'abonements': abonements,
        'title': 'Абонементы',
    }
    return render(request, 'webGym/gate_abonements.html', context)


@login_required
@gate_permission_required()
@require_POST
def gate_abonement_delete(request, pk):
    ab = get_object_or_404(Abonement, pk=pk)
    ab.delete()
    messages.success(request, 'Абонемент удалён.')
    return redirect('gate_abonements')


# ---------------------------------------------------------------------------
# Тренеры (CRUD) — доступно оператору проходной
# ---------------------------------------------------------------------------
@login_required
@gate_permission_required()
def trainer_list(request):
    trainers = (Trainer.objects
                .select_related('user')
                .order_by('user__last_name', 'user__first_name'))
    context = {
        'trainers': trainers,
        'title': 'Тренеры',
    }
    return render(request, 'webGym/trainer_list.html', context)


@login_required
@gate_permission_required()
def trainer_add(request):
    if request.method == 'POST':
        form = TrainerUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data.get('email') or '',
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
            )
            user.groups.add(_trainer_group())
            Trainer.objects.create(
                user=user,
                phone=data.get('phone') or '',
                specialization=data['specialization'],
                experience_years=data['experience_years'],
            )
            messages.success(request, f'Тренер «{user.username}» добавлен.')
            return redirect('trainer_list')
    else:
        form = TrainerUserForm()
    context = {'form': form, 'title': 'Добавить тренера'}
    return render(request, 'webGym/trainer_form.html', context)


@login_required
@gate_permission_required()
def trainer_delete(request, pk):
    if request.method == 'POST':
        trainer = get_object_or_404(Trainer, pk=pk)
        username = trainer.user.username
        trainer.user.delete()
        messages.success(request, f'Тренер «{username}» удалён.')
    return redirect('trainer_list')