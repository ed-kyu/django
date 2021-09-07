from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 생성될 때니까 add 붙음..
    updated_at = models.DateTimeField(auto_now=True)