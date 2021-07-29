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
        verbose_name='почта')
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='никнейм')
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='пользователь'
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'following'],
            name='unique_subscriptions')]

        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
