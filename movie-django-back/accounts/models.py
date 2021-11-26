from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from movies.models import Movie

def get_user_path(instance, filename):
    return f"profile/{instance.username}/{filename}"

# Create your models here.
class User(AbstractUser):
    hearts = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    photo = models.ImageField(upload_to=get_user_path, default="default/image.jpg",)
    message = models.CharField(max_length=200, default="프로필 메시지를 입력하세요")
    like = models.ManyToManyField(Movie, related_name="like_users")
    dislike = models.ManyToManyField(Movie, related_name="dislike_users")

    def __str__(self):
        return self.username
    
    # def save(self, *args, **kwargs):
    #     if self.id is None:
    #         temp = self.photo
    #         self.photo = None
    #         super().save(*args, **kwargs)
    #         self.photo = temp
    #     super().save(*args, **kwargs)
        
