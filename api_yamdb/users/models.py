from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс для пользователей."""

    ROLES_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    ]
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
    )
    bio = models.TextField(verbose_name='Биография', blank=True,)
    role = models.CharField(
        verbose_name='Роль',
        max_length=10,
        choices=ROLES_CHOICES,
        default='user',
    )

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    class Meta:
        ordering = ['username']
