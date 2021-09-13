from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_OF_USER_CHOICES = [
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    ]

    email = models.EmailField(
        max_length=254,
        verbose_name="Электропочта",
        blank=False,
        unique=True,
    )

    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
        null=True,
    )

    role = models.CharField(
        verbose_name="Роль",
        max_length=9,
        choices=ROLE_OF_USER_CHOICES,
        default="user",
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
        return self.role == "user"

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_admin(self):
        return self.role == "admin"
