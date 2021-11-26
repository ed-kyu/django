from django.db import models
from django.conf import settings
# Create your models here.
from movies.models import Movie
class Review(models.Model):
    RATES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews',)
    #like_user = models.ManyToManyField(AbstractUser, related_name='like_users')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=100)
    content = models.TextField()
    rate = models.IntegerField(choices=RATES, default=5)
    # like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    # dislike = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.content}'

class Rate(models.Model):
    RATES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rates')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='rates')
    rate = models.IntegerField(choices=RATES, default=5)

    def __str__(self):
        return f'{self.rate}'