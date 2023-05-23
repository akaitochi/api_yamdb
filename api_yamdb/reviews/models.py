from django.db import models

from .validators import validate_year


class Categories():
    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра'
    )

    class Meta:
        verbose_name = 'Категория'


class Genres(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра'
    )

    class Meta:
        verbose_name = 'Жанр'


class Titles(models.Model):
    name = models.CharField(
        max_length=200,
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
        Genres,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='titles'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведения'

    def __str__(self):
        return self.name
