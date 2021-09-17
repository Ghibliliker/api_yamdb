from django.core.validators import RegexValidator
from django.db import models
from django.db.models.deletion import CASCADE

from users.models import User
from .validators import raiting_validator, year_validator

SLUG_REGEX = RegexValidator(r'^[-a-zA-Z0-9_]+$', 'неподходящий "slug"')


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='name of category')
    slug = models.SlugField(
        verbose_name='slug of category',
        validators=[SLUG_REGEX],
        unique=True,
        max_length=50
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=500, verbose_name='name of genre')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='slug of genre'
    )

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(db_index=True, verbose_name='name of title')
    year = models.IntegerField('year', validators=[year_validator])
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='description of title'
    )
    genre = models.ManyToManyField(Genre, verbose_name='genres of title')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        verbose_name='category of title',
        related_name='titles', null=True)

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

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
        help_text='Напишите текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='review author',
        related_name='reviews'
    )
    score = models.IntegerField(
        'review score',
        validators=[raiting_validator]
    )
    pub_date = models.DateTimeField('review date', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [models.UniqueConstraint(fields=['author', 'title'],
                       name='1_review_per_author')]
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='comment review',
        related_name='comments'
    )
    text = models.TextField(
        'comment text',
        blank=False,
        help_text='Напишите комментарий',
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
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
