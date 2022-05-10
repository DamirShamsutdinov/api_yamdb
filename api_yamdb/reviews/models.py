from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    roles = ()
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField('Email', max_length=254, unique=True)
    role = models.CharField(
        max_length=150,
        blank=True
    )
    bio = models.TextField()
    def __str__(self):
        return str(self.username)


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
    id = models.AutoField(primary_key=True)
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
    score = models.IntegerField()
    

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

    def __str__(self):
        return self.author