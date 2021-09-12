from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models.deletion import CASCADE
import datetime

from users.models import User

SLUG_REGEX = RegexValidator(r'^[-a-zA-Z0-9_]+$', 'неподходящий "slug"')


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        validators=[SLUG_REGEX],
        unique=True,
        max_length=50
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(
        'year',
        validators=[
            MinValueValidator(-10000),
            MaxValueValidator(datetime.date.today().year)
        ]
    )
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='category', null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='reviewed title',
        related_name='reviews'
    )
    text = models.TextField(
        'review text',
        blank=False,
        help_text='Напишите текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='review author',
        related_name='reviews'
    )
    score = models.IntegerField(
        'review score',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('review date', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    reviews = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='comment review',
        related_name='comments'
    )
    text = models.TextField(
        'comment text',
        blank=False,
        help_text='Напишите комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='comment author',
        related_name='comments'
    )
    pub_date = models.DateTimeField('date of comment', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
