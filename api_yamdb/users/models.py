from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from .confirmation_code import create_code


class UserManager(BaseUserManager):
    def create_user(self, username, bio, email, role="US", password=None):
        print(f"create_user: email={email}, role={role}")
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role,
            bio=bio
        )

        conf_code = create_code(user)

        user.save(using=self._db)

        user.confirmation_code = conf_code

        user.save(using=self._db)

        return user

    def create_superuser(self, username, bio, email, role="AD", password=None):
        print(f"create_superuser: email={email}")
        user = self.create_user(
            username,
            email=email,
            role=role,
            bio=bio
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    USER = "US"
    MODERATOR = "MO"
    ADMIN = "AD"
    ROLE_OF_USER_CHOICES = [
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    ]

    objects = UserManager()

    email = models.EmailField(
        max_length=254,
        verbose_name="Электропочта",
        blank=False,
        unique=True,
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

    confirmation_code = models.CharField(
        verbose_name='Confirmation code',
        max_length=30,
        blank=True,
    )
