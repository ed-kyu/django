from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes 
from rest_framework import status
from rest_framework.response import Response
from .serializers import ReviewListSerializer, ReviewSerializer, CommentSerializer, CommentListSerializer, RateSerializer
from movies.serializers import ActorSerializer, ActorListSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Rate, Review, Comment
from movies.models import Actor, Movie
from accounts.serializers import IdentificationSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def my_reviews_list(request, user_pk):
    reviews = Review.objects.filter(user_id=user_pk)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def reviews_list_or_create(request, movie_pk):
    if request.method == 'GET':
        reviews = Review.objects.filter(movie_id=movie_pk).order_by('-pk')
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)    
        user = get_object_or_404(get_user_model(), username=request.user)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)
            return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JSONWebTokenAuthentication,))
# def create_review(request, movie_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)    
#     serializer = ReviewSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(movie=movie, user=request.user)
#         return Response(serializer.data)
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def reviews_update_or_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)   

    def review_update():
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


    def review_delete():
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        return review_update()
    elif request.method == 'DELETE':
        return review_delete()


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def actor_detail(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)

    def actor_detail():
        serializer = ActorSerializer(actor)
        return Response(serializer.data)

    if request.method == 'GET':
        return actor_detail()



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def actors_list_or_create(request):

    if request.method == 'GET':
        actors = Actor.objects.all()
        serializer = ActorListSerializer(actors, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ActorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def comment_create_or_list(request, review_pk):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_pk)    
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review=review, user=request.user)
            return Response(serializer.data)

    elif request.method == 'GET':
        comments = Comment.objects.filter(review=review_pk).order_by('-pk')
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def comment_update_or_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)   

    if request.method == 'PUT':
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def rate_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = RateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def rate_list(request, movie_pk, user_pk):
        try:
            rate = Rate.objects.filter(user_id=user_pk).get(movie_id=movie_pk)
            serializer = RateSerializer(rate)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def rate_update_or_delete(request, rate_pk):
    rate = get_object_or_404(Rate, pk=rate_pk)

    if request.method == 'PUT':
        serializer = RateSerializer(instance=rate, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)