from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),
    path('detail/<int:movie_pk>/', views.movie_detail),
    path('genres/', views.movie_genres_list),
    path('detail/<int:movie_pk>/like/', views.like),
    path('detail/<int:movie_pk>/dislike/', views.dislike),
]