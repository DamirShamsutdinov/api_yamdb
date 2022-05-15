from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLES = [
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
    (USER, 'Пользователь')
]


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Поле email должно быть заполнено')
        if username == 'me':
            raise ValueError('ИЗапрещено использовать имя пользователя "me"')
        return super().create_user(
            username, email=email, password=password, **extra_fields
        )

    def create_superuser(
            self, username, email, password, role, **extra_fields):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields)


class User(AbstractUser):
    """Модель пользователя"""
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    email = models.EmailField(
        unique=True,
        verbose_name='E-mail',
    )
    password = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name='Пароль'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя',
    )
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        ordering = ('id',)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
