from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='Слаг категории'
    )

    class Meta:
        verbose_name = 'Категория'


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='Слаг жанра'
    )
    on_delete = models.CASCADE

    class Meta:
        verbose_name = 'Жанр'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название'
    )
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='titles'
    )
    on_delete = models.CASCADE

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведения'

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLES_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    ]
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
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

    # @property
    # def is_superuser(self):
    #     return self.role == "admin"
