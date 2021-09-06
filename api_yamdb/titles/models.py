from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime

class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

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
    )
    description = models.TextField(null=True, blank=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genre')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='category')

    def __str__(self):
        return self.name