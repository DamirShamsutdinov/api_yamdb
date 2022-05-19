from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User


class Genre(models.Model):
    """Модель Жанров"""

    name = models.CharField(
        max_length=256,
        verbose_name="Название жанра",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="поле слаг_Жанр",
    )

    def __str__(self):
        return self.slug


class Category(models.Model):
    """Модель Категорий"""

    name = models.CharField(
        max_length=256,
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="поле слаг_Категория",
    )

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название произведения",
    )
    year = models.PositiveSmallIntegerField(verbose_name="Год издания", )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name="Категория_произведения",
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="titless",
        verbose_name="Жанр_произведения",
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Описание произведения",
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель Отзывов"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение с отзывом",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата отзыва",
    )
    text = models.TextField(
        help_text="Введите текст отзыва",
        verbose_name="Текст отзыва",
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, "Минимальная оценка - 1"),
            MaxValueValidator(10, "Максимальная оценка - 10"),
        ],
        verbose_name="Оценка произведения",
    )

    class Meta:
        ordering = ("-pub_date",)
        constraints = [
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
        related_name="comments",
        verbose_name="Отзыв с комментарием",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author",
        verbose_name="Автор комментария",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата комментария",
    )
    text = models.TextField(verbose_name="Текст комментария",)

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text
