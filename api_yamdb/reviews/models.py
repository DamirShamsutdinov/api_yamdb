from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser
from django.db.models import CheckConstraint, Q, UniqueConstraint



ROLE = (('admin', 'admin'), ('moderator', 'moderator'), ('user', 'user'))


class User(AbstractUser):
    bio = models.TextField('Биография', blank=True, )
    role = models.CharField(max_length=16, choices=ROLE, default='user')


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
        )

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
        )

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=30)
    year = models.PositiveIntegerField()
    description = models.TextField(
        blank=True,
        null=True,
        )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles'
    )
    rating = models.IntegerField(
        null=True,
        default=None
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        related_name='titles',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    id = models.AutoField(primary_key=True)
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
        'Дата отзыва',
        auto_now_add=True,
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Максимальная оценка - 10')
        ]
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(score__range=(0, 10)),
                name='valid_rate'
            ),
            UniqueConstraint(
                fields=["author", "title"],
                name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
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
        'Дата публикации комментария',
        auto_now_add=True,
    )
    text = models.TextField()

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text