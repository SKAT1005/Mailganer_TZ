# coding=utf-8
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, name='Электронная почта')
    first_name = models.CharField(max_length=256, name='Имя пользователя')
    last_name = models.CharField(max_length=256, name='Фамилия пользователя')
    birthday = models.DateField(name='День рождения')
    mails = models.ForeignKey('Mail', blank=True, name='Письма пользователя', on_delete=models.CASCADE)

    def get_full_name(self):
        return str(self.last_name + ' ' + self.first_name)

    def get_short_name(self):
        return self.first_name


class Mail(models.Model):
    user = models.OneToOneField('User', name='Пользователь')
    text = models.CharField(max_length=2 ** 20, blank=True, name='Текст письма')
    status = models.BooleanField(default=False, name='Статус письма')

    def __str__(self):
        if self.status:
            return 'Письмо прочитано'
        else:
            return 'Письмо не прочитано'
