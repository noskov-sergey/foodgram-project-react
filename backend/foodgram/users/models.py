from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'логин',
        unique=True,
        max_length=150,
    )
    password = models.CharField(
        'пароль',
        max_length=150,
    )
    email = models.EmailField(
        'email',
        unique=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


    def __str__(self):
        return self.username