
from django.shortcuts import get_object_or_404
from rest_framework.response  import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Genre
from .serializers import MovieSerializer, MovieDetailSerializer, GenreSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def movie_list(request):
    movies = Movie.objects.all().order_by('release_date', 'popularity').reverse()[:100]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def movie_genres_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def like(request, movie_pk):
    fan = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if not fan.dislike.filter(pk=movie_pk).exists():
        if fan.like.filter(pk=movie_pk).exists():
            fan.like.remove(movie)
            is_loved = False
        else:
            fan.like.add(movie)
            is_loved = True

    context = {
        # "isLoved": is_loved,
        "likesReceived": movie.like_users.count()
    }
    return Response(context)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def dislike(request, movie_pk):
    fan = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if not fan.like.filter(pk=movie_pk).exists():
        if fan.dislike.filter(pk=movie_pk).exists():
            fan.dislike.remove(movie)
            is_loved = False
        else:
            fan.dislike.add(movie)
            is_loved = True

    context = {
        # "isHated": is_loved,
        "dislikesReceived": movie.dislike_users.count()
    }
    return Response(context)