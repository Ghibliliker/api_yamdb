from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
import datetime

SLUG_REGEX = RegexValidator(r'^[-a-zA-Z0-9_]+$', 'неподходящий "slug"')

class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        validators=[SLUG_REGEX],
        unique=True, 
        max_length=50
    )  # ^[-a-zA-Z0-9_]+$  тест адекватности

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
        validators=[MinValueValidator(-10000), MaxValueValidator(datetime.date.today().year)]
    )           # реализовать в сериализаторе?
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='category')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
