from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q

ROLE = (('admin', 'admin'), ('moderator', 'moderator'), ('user', 'user'))


class User(AbstractUser):
    """Модель Пользователя"""
    bio = models.TextField('Биография', blank=True, )
    role = models.CharField('Роль', max_length=16, choices=ROLE,
                            default='user')
    confirmation_code = models.CharField(
        'Код потдверждения',
        max_length=36,
        null=True,
        blank=True
    )


class Genre(models.Model):
    """Модель Жанров"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Category(models.Model):
    """Модель Категорий"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель Произведений"""
    name = models.CharField('Название', max_length=30)
    year = models.PositiveIntegerField('Год издания',)
    rating = models.IntegerField(
        'Рейтинг',
        default=None,
        null=True,
        blank=True
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
    )
    genre = models.ForeignKey(
        'Жанр',
        Genre,
        blank=True,
        null=True,
        related_name='titles',
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        'Категория',
        Category,
        blank=True,
        null=True,
        related_name='titles',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель Отзывов"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True,
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Максимальная оценка - 10')
        ]
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            CheckConstraint(
                check=Q(score__range=(0, 10)),
                name='valid_rate'
            ),
            UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель Комментариев"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='review'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
    )
    text = models.TextField()

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
