from rest_framework import serializers
from .models import Rate, Review, Comment
from movies.models import Movie
from django.contrib.auth import get_user_model


# 전체 리뷰 목록
class ReviewListSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'username',)

    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ('content', 'created_at', 'id', 'movie', 'rate', 'title', 'updated_at', 'user',)


# 단일 리뷰 정보
class ReviewSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'username',)

    user = UserSerializer(read_only=True)

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = '__all__'

    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('pk', 'title', 'content', 'rate', 'movie', 'created_at', 'updated_at', 'user', )
        read_only_fields = ('created_at',)

class CommentSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'username',)

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'review', 'content', 'created_at', 'updated_at',)
        read_only_fields = ('user', 'review', 'created_at',)

class CommentListSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'username',)

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'



class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'