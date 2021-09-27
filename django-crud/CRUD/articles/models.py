from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d') # 연월일로 구분저장
    created_at = models.DateTimeField(auto_now_add=True) # 생성될 때니까 add 붙음..
    updated_at = models.DateTimeField(auto_now=True)
