from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from . import views


urlpatterns = [
    path('signup/', views.signup),
    path('api-token-auth/', obtain_jwt_token), # login
    path('identify/', views.identify),
    path('<username>/', views.get_profile),
    path('update/', views.update_profile),
    path('<username>/follow/', views.follow),
    path('<username>/favorites/', views.get_favorites),
    path('<username>/recommendbyprofile/', views.get_recommend),
] 