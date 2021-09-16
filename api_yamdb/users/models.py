from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_OF_USER_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    email = models.EmailField(
        max_length=254,
        verbose_name='Электропочта',
        blank=False,
        unique=True,
    )

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=9,
        choices=ROLE_OF_USER_CHOICES,
        default=self.USER,
    )

    confirmation_code = models.CharField(
        max_length=30,
        blank=True,
        editable=False,
        null=True,
        unique=True
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
