from django.contrib import admin

# Register your models here.
from .models import Review, Comment, Rate

admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Rate)