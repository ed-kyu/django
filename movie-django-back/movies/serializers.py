from rest_framework import serializers
from .models import Movie, Actor, Genre

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('overview',)


class MovieDetailSerializer(serializers.ModelSerializer):
    def get_loved(self, movie):
        return movie.like_users.count()

    def get_hated(self, movie):
        return movie.dislike_users.count()

    loved = serializers.SerializerMethodField("get_loved")
    hated = serializers.SerializerMethodField("get_hated")

    class Meta:
        model = Movie
        fields = "__all__"


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name',)

class ActorSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title',)

    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ('id', 'name', 'movies')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'
        # fields = ('id', 'title', 'completed',)