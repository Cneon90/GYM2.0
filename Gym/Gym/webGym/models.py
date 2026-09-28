from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils import timezone


# Create your models here.
class main_icon(models.Model):
    image_src = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    titile = models.CharField(max_length=255, null=True)
    text = models.CharField(max_length=255, null=True)
    Position = models.IntegerField(null=True)

    def __str__(self):
        return self.text


class MainMenu(models.Model):
    Alias = models.CharField(max_length=255, null=True)
    Name = models.CharField(max_length=20, null=True)
    Position = models.IntegerField(null=True)

    def __str__(self):
        return self.Name


class banner(models.Model):
    Titile = models.CharField(max_length=255, null=True)
    text = models.CharField(max_length=255, null=True)
    image_src = models.CharField(max_length=255, null=True)
    Position = models.IntegerField(null=True)

    def __str__(self):
        return self.Titile


class banner_button(models.Model):
    Slide = models.ForeignKey(banner, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, null=True)
    text = models.CharField(max_length=255, null=True)
    Position = models.IntegerField(null=True)

    def __str__(self):
        return self.text


# ---------------------------------------------------------------------------
#  Модуль «Проходная» (оператор проходной)
# ---------------------------------------------------------------------------

class Abonement(models.Model):
    """Абонемент члена клуба для проверки на проходной."""
    TYPE_VISITS = 'visits'      # лимит по числу посещений
    TYPE_MONTH = 'month'        # безлимит на месяц
    TYPE_YEAR = 'year'          # безлимит на год
    TYPE_CHOICES = [
        (TYPE_VISITS, 'По числу посещений'),
        (TYPE_MONTH, 'Безлимит на месяц'),
        (TYPE_YEAR, 'Безлимит на год'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='abonements',
                             verbose_name='Пользователь')
    abo_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_MONTH,
                                verbose_name='Тип абонемента')
    start_date = models.DateField(default=timezone.now, verbose_name='Начало действия')
    end_date = models.DateField(null=True, blank=True, verbose_name='Конец действия')
    max_visits = models.PositiveIntegerField(default=0, verbose_name='Лимит посещений',
                                             help_text='Для типа «по числу посещений»')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'
        permissions = [
            ('can_manage_gate', 'Может работать на проходной'),
            ('can_manage_trainers', 'Может управлять тренерами'),
        ]

    def __str__(self):
        return f'{self.user} — {self.get_abo_type_display()}'

    @property
    def is_active(self):
        """Абонемент действует (по сроку и/или лимиту)."""
        today = timezone.localdate()
        if self.abo_type in (self.TYPE_MONTH, self.TYPE_YEAR):
            if self.end_date and today > self.end_date:
                return False
            return True
        # по числу посещений: проверяем остаток
        return self.remaining_visits > 0

    @property
    def remaining_visits(self):
        if self.abo_type != self.TYPE_VISITS:
            return None  # безлимит
        used = self.visits.filter(abonement=self).count()
        return max(0, self.max_visits - used)

    @property
    def status_text(self):
        if not self.is_active:
            if self.abo_type == self.TYPE_VISITS:
                return 'Посещения истекли'
            return 'Просрочен'
        return 'Действует'


class Visit(models.Model):
    """Отметка входа члена клуба на проходной."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits',
                             verbose_name='Пользователь')
    abonement = models.ForeignKey(Abonement, null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='visits', verbose_name='Абонемент')
    entered_at = models.DateTimeField(auto_now_add=True, verbose_name='Время входа')
    operator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='recorded_visits', verbose_name='Оператор проходной')

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'
        ordering = ['-entered_at']

    def __str__(self):
        return f'{self.user} — {self.entered_at.strftime("%d.%m.%Y %H:%M")}'


class Trainer(models.Model):
    """Тренер клуба. Привязан к пользователю системы (аккаунту)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile',
                                verbose_name='Пользователь')
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name='Телефон')
    specialization = models.CharField(max_length=120, blank=True, null=True,
                                      verbose_name='Специализация')
    experience_years = models.PositiveIntegerField(default=0, verbose_name='Стаж (лет)')

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'

    def __str__(self):
        return self.user.username


# Добавляем в админку

admin.site.register(MainMenu)
admin.site.register(banner)
admin.site.register(banner_button)
admin.site.register(main_icon)
admin.site.register(Abonement)
admin.site.register(Visit)
admin.site.register(Trainer)
