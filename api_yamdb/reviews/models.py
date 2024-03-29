from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .validators import validate_year

VALIDATOR_MESSAGE = 'Оценка от 1 до 10'
CHARFIELDMAXLENGTH = 256
SLUGFIELDMAXLENGTH = 50


class Category(models.Model):
    """Класс для категорий произведений."""

    name = models.CharField(
        max_length=CHARFIELDMAXLENGTH,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=SLUGFIELDMAXLENGTH,
        unique=True,
        db_index=True,
        verbose_name='Слаг категории'
    )

    class Meta:
        verbose_name = 'Категория'
        ordering = ('name',)


class Genre(models.Model):
    """Класс для жанров произведений."""

    name = models.CharField(
        max_length=CHARFIELDMAXLENGTH,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=SLUGFIELDMAXLENGTH,
        unique=True,
        db_index=True,
        verbose_name='Слаг жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        ordering = ('name',)


class Title(models.Model):
    """Класс для произведений."""

    name = models.CharField(
        max_length=CHARFIELDMAXLENGTH,
        db_index=True,
        verbose_name='Название'
    )
    year = models.PositiveIntegerField(
        db_index=True,
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
        blank=True,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
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
        return self.name[:20]


class Review(models.Model):
    """Отзыв произведения."""

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, VALIDATOR_MESSAGE),
            MaxValueValidator(10, VALIDATOR_MESSAGE)
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    """Комментарий к отзыву произведения."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ['pub_date']
