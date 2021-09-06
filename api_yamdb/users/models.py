from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = "US"
    MODERATOR = "MO"
    ADMIN = "AD"
    ROLE_OF_USER_CHOICES = [
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    ]

    email = models.EmailField(
        max_length=254,
        verbose_name="Электропочта",
        blank=False,
    )

    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )

    role = models.CharField(
        verbose_name="Роль",
        max_length=2,
        choices=ROLE_OF_USER_CHOICES,
        default=USER,
    )
