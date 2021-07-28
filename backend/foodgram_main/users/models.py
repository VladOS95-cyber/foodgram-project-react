from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    GUEST = 'guest', 'Гость'
    USER = 'user', 'Пользователь'
    ADMIN = 'admin', 'Администратор'


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    role = models.CharField('Роль', max_length=150, choices=Role.choices,
                            default=Role.GUEST)
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='email')
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='username')
    first_name = models.CharField(max_length=150, verbose_name='first_name')
    last_name = models.CharField(max_length=150, verbose_name='last_name')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='user'
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='author'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'following'],
            name='unique_subscriptions')
    ]
        verbose_name = 'subscription'
        verbose_name_plural = 'subscriptions'
