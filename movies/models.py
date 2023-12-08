from datetime import datetime

from django.db import models


class Director(models.Model):
    year = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def age(self):
        return datetime.now().year - self.year


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE,
                                 null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    rating = models.FloatField()
    year = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def genre_list(self):
        return [genre.name for genre in self.genres.all()]


STARS = (
    (i, '* ' * i) for i in range(1, 6)
)


class Review(models.Model):
    text = models.TextField(null=True)
    stars = models.IntegerField(choices=STARS)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='reviews')

    def __str__(self):
        return self.text
