from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    ]
    bio = models.TextField('Биография', blank=True,)
    role = models.CharField(
        max_length=10,
        choices=ROLES_CHOICES,
        default='user',
    )

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_superuser(self):
        return self.role == "admin"
