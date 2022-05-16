from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE = [
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
    (USER, 'Пользователь')
]


class User(AbstractUser):
    """Модель Пользователя"""
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    role = models.CharField(
        max_length=16,
        choices=ROLE,
        default=USER,
        verbose_name='Роль пользователя',
    )
    confirmation_code = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        verbose_name='Код потдверждения',
    )
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        ordering = ('id',)
