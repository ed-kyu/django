from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.pk}: {self.name}'


class Movie(models.Model):
    title = models.CharField(max_length=200,)
    poster_path = models.TextField(blank=True)
    popularity = models.FloatField()
    overview = models.TextField()
    vote_average = models.FloatField()
    release_date = models.DateTimeField()
    runtime = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies")

    def __str__(self):
        return self.title

class Actor(models.Model):
    name = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie, related_name='actors')

    def __str__(self):
        return f'{self.pk}: {self.name}'
