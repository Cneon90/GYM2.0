from django import forms

from .models import *
from django.core.exceptions import ValidationError


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'input is-success'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input'}))


class AbonementForm(forms.ModelForm):
    """Форма создания/редактирования абонемента."""
    username = forms.CharField(
        label='Логин пользователя',
        required=True,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Логин члена клуба'}),
    )

    class Meta:
        model = Abonement
        fields = ['abo_type', 'start_date', 'end_date', 'max_visits']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.DateInput(
            attrs={'class': 'input', 'type': 'date'})
        self.fields['end_date'].widget = forms.DateInput(
            attrs={'class': 'input', 'type': 'date'})
        self.fields['start_date'].label = 'Начало действия'
        self.fields['end_date'].label = 'Конец действия (для безлимитов)'
        self.fields['max_visits'].label = 'Лимит посещений (для «по числу»)'

    def clean(self):
        cleaned = super().clean()
        abo_type = cleaned.get('abo_type')
        if abo_type in (Abonement.TYPE_MONTH, Abonement.TYPE_YEAR):
            if not cleaned.get('end_date'):
                self.add_error('end_date', 'Укажите дату окончания для этого типа абонемента.')
        elif abo_type == Abonement.TYPE_VISITS:
            if not cleaned.get('max_visits') or cleaned['max_visits'] <= 0:
                self.add_error('max_visits', 'Укажите положительное число посещений.')
        return cleaned

    def save(self, commit=True):
        username = self.cleaned_data.get('username', '').strip()
        obj = super().save(commit=False)
        if username:
            user = User.objects.filter(username__iexact=username).first()
            if not user:
                raise forms.ValidationError(f'Пользователь «{username}» не найден.')
            obj.user = user
        if commit:
            obj.save()
        return obj


class TrainerUserForm(forms.Form):
    """Форма создания тренера: аккаунт + профиль тренера."""
    username = forms.CharField(label='Логин', max_length=150,
                               widget=forms.TextInput(attrs={'class': 'input'}))
    first_name = forms.CharField(label='Имя', max_length=150,
                                 widget=forms.TextInput(attrs={'class': 'input'}))
    last_name = forms.CharField(label='Фамилия', max_length=150,
                                widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(label='Email', required=False,
                             widget=forms.EmailInput(attrs={'class': 'input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'input'}))
    phone = forms.CharField(label='Телефон', max_length=30, required=False,
                            widget=forms.TextInput(attrs={'class': 'input'}))
    specialization = forms.CharField(label='Специализация', max_length=120,
                                     widget=forms.TextInput(attrs={'class': 'input'}))
    experience_years = forms.IntegerField(label='Стаж (лет)', min_value=0, initial=0,
                                          widget=forms.NumberInput(attrs={'class': 'input'}))

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Логин уже занят.')
        return username