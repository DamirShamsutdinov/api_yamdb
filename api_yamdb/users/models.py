from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель Пользователя"""
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLE = [
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь")
    ]
    REQUIRED_FIELDS = ["email", "password"]

    bio = models.TextField(
        blank=True,
        verbose_name="Биография",
    )
    role = models.CharField(
        max_length=16,
        choices=ROLE,
        default=USER,
        verbose_name="Роль пользователя",
    )
    confirmation_code = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        verbose_name="Код потдверждения",
    )

    class Meta:
        ordering = ("id",)
