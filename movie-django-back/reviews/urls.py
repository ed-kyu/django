from django.urls import path
from . import views

urlpatterns = [
    path('actors/', views.actors_list_or_create),
    path('actors/<int:actor_pk>/', views.actor_detail), 
    # path('movies/reviews/', views.reviews_list),
    # path('movies/<int:movie_pk>/create/', views.create_review), # 리뷰 생성
    path('myreviews/<int:user_pk>/', views.my_reviews_list), # 개인 유저 모든 리뷰 가져오기..
    path('movies/<int:movie_pk>/', views.reviews_list_or_create),
    path('<int:review_pk>/', views.reviews_update_or_delete),
    path('<int:review_pk>/detail/', views.review_detail),
    #
    path('movies/<int:movie_pk>/createrate/', views.rate_create),
    path('movies/<int:movie_pk>/<int:user_pk>/', views.rate_list),
    path('rates/<int:rate_pk>/', views.rate_update_or_delete),

    path('<int:review_pk>/comments/', views.comment_create_or_list),
    path('comments/<int:comment_pk>/', views.comment_update_or_delete),
]