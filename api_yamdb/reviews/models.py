from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


from .validators import validate_year

VALIDATOR_MESSAGE = 'Оценка от 1 до 10'

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
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        blank=False,
        unique=True,
        null=False
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
        return self.role == "moderator"

    @property
    def is_admin(self):
        return self.role == "admin"

    # @property
    # def is_superuser(self):
    #     return self.role == "admin"


class Review(models.Model):
    """Отзыв произведения."""
    title = models.ForeignKey(
        Titles,
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
