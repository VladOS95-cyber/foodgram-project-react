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
    email = models.EmailField(max_length=254, unique=True, blank=False)
    username = models.CharField(max_length=150, unique=True, blank=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_subscribed = models.BooleanField(blank=True, null=False, default=False)


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        unique_together = ['user', 'following']
