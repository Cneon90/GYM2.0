from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


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


# Добавляем в админку

admin.site.register(MainMenu)
admin.site.register(banner)
admin.site.register(banner_button)
admin.site.register(main_icon)
