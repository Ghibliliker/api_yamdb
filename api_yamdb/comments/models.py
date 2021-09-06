from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator


from titles.models import Title
from users.models import User


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
