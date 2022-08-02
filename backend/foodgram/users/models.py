from django.contrib.auth.models import AbstractUser
from django.db import models


class FoodgramUser(AbstractUser):
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
        help_text='Введите адрес электронной почты',
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['username']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        related_name='follower',
        verbose_name='подписчик',
        on_delete=models.CASCADE,
        help_text='подписчик',
    )
    author = models.ForeignKey(
        FoodgramUser,
        related_name='following',
        verbose_name='Отслеживаемый автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'подписка на автора'
        verbose_name_plural = 'подписки на авторов'
        unique_together = (
            ('user', 'author'),
        )
    
    def __str__(self):
        return f'{self.user} follows {self.author}'