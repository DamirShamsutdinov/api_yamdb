from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = (('admin', 'admin'), ('moderator', 'moderator'), ('user', 'user'))


class User(AbstractUser):
    bio = models.TextField('Биография', blank=True, )
    role = models.CharField(max_length=16, choices=ROLE, default='user')


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    year = models.PositiveIntegerField()
    rating = models.IntegerField(default=None, null=True,
                                 blank=True)  # нужно отдельную вьюху сделать к нему, среднюю оценку от 1 до 10 по оценки(score) в отзывах(Review)
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        related_name='genres',
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        related_name='reviews',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    # a = list(range(11))
    # RAITING = dict(zip(a, a))
    RAITING = (
        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
        ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'))
    id = models.AutoField(primary_key=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.SmallIntegerField('Рейтинг', default=0,
                                     choices=RAITING)
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True,
    )


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True,
    )
    text = models.TextField()

    def __str__(self):
        return self.author
