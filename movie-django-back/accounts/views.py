from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer, IdentificationSerializer
from movies.serializers import MovieSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
	# 1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
		
	# 1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
	# 2. UserSerializer를 통해 데이터 직렬화
    serializer = UserSerializer(data=request.data)
    
	# 3. validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        #4. 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()
        # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다. (write_only)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def identify(request):
    who = request.user

    serializer = IdentificationSerializer(instance=who, )
    return Response(serializer.data)
    

@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET'])
def get_profile(request, username):
    person = request.user
    if username != "undefined":
        person = get_object_or_404(get_user_model(), username=username)

    serializer = ProfileSerializer(instance=person,)
    return Response(serializer.data)


@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['PUT'])
def update_profile(request):
    return Response()


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def follow(request, username):
    me = request.user
    you = get_object_or_404(get_user_model(), username=username)

    if you != me:
        if you.followers.filter(pk=me.pk).exists():
            you.followers.remove(me)
            is_followed = False
        else:
            you.followers.add(me)
            is_followed = True

        context = {
            "isFollowed" : is_followed,
            "HeartsReceived": you.followers.count(),
            "HeartsSending": you.hearts.count(),
        }
        return Response(context)


@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET'])
def get_favorites(request, username):
    who = get_object_or_404(get_user_model(), username=username)
    favorites = who.like.all()
    serializer = MovieSerializer(favorites, many=True)
    return Response(serializer.data)



import os
import sys
import requests
import json
@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET'])
def get_recommend(request, username):
    
    TMDB_KEY = os.environ.get("TMDB_KEY")
    NAVER_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID")
    NAVER_CLIENT_KEY = os.environ.get("NAVER_CLIENT_KEY")

    results = []
    client_id = NAVER_CLIENT_ID
    client_secret = NAVER_CLIENT_KEY
    img_name = 'image.jpg'
    url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식
    files = {'image': open(f'./media/default/{img_name}', 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code
    if(rescode==200):
        data = json.loads(response.text)
        for i in range(data['info']['faceCount']):
            celebrity = data['faces'][0]['celebrity']['value']
            similarity = data['faces'][0]['celebrity']['confidence']
            print(f'{celebrity} {similarity*100}% 닮음!!')
            
            url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json"
            params = {'key': '036a05f62fa6a8bfbe2c4605b94e42d9', 'peopleNm': f'{celebrity}' }
            response = requests.get(url, params=params)
            data_num = 0
            if response.status_code==200:
                data = json.loads(response.text)
                data_num = data['peopleListResult']['totCnt']
            if data_num:
                for curPage in range(1, data_num//10+2):
                    params = {'key': '036a05f62fa6a8bfbe2c4605b94e42d9', 'peopleNm': f'{celebrity}', 'curPage': curPage }
                    response = requests.get(url, params=params)
                    if response.status_code==200:
                        data = json.loads(response.text)
                        if curPage*10 <= data_num:
                            for i in range(10):
                                people_job = data['peopleListResult']['peopleList'][i]['repRoleNm']
                                if people_job == '배우':
                                    peopleCd = data['peopleListResult']['peopleList'][i]['peopleCd']
                                    peopleNm = data['peopleListResult']['peopleList'][i]['peopleNm']
                                    # print(f'{peopleNm}의 코드는 {peopleCd}')
                                    filmos = data['peopleListResult']['peopleList'][i]['filmoNames'].split('|')
                                    # print(filmos)
                                    results.extend(filmos)
                        elif curPage*10 > data_num:
                            for i in range(data_num-(curPage-1)*10):
                                people_job = data['peopleListResult']['peopleList'][i]['repRoleNm']
                                if people_job == '배우':
                                    peopleCd = data['peopleListResult']['peopleList'][i]['peopleCd']
                                    peopleNm = data['peopleListResult']['peopleList'][i]['peopleNm']
                                    print(f'{peopleNm}의 코드는 {peopleCd}')
                                    filmos = data['peopleListResult']['peopleList'][i]['filmoNames'].split('|')
                                    # print(filmos)
                                    results.extend(filmos)

    else:
        print(f"Error Code: {rescode}")

    print('필모그래피 검색 결과', results)




    class Tmdb_API:
        key = TMDB_KEY
        url = 'https://api.themoviedb.org/3/search/movie/'
        
        def __init__(self, id):
            self.id = id
            self.query = f"{Tmdb_API.url}?api_key={Tmdb_API.key}&language=ko-KR&include_adult=false&query='{self.id}'"

    movie_result = []

    for fimo_title in results:
        query = Tmdb_API(fimo_title).query
        # print(query)
        res = requests.get(query)
        if res.status_code == 200:
            movie = res.json()
            # print(movie)
            for i in range(movie['total_results']):
                try:
                    # print(movie['results'][i]['original_language'], movie['results'][i]['popularity'])
                    if movie['results'][i]['original_language'] == 'ko':
                        if movie['results'][i]['popularity'] > 6:
                            title = movie['results'][i]['title']
                            poster_path = movie['results'][i]['poster_path']
                            release_date = movie['results'][i]['release_date']
                            popularity = movie['results'][i]['popularity']
                            movie_result.append(
                                {
                                    'celebrity': celebrity,
                                    'similarity': similarity,
                                    'title': title,
                                    'poster_path' : poster_path,
                                    'release_date' : release_date,
                                    'popularity': popularity,

                                }
                            )
                except:
                    continue

    print(movie_result)
    # with open("recommend.json", 'w') as JSON:
    #     json.dump(movie_result, JSON, ensure_ascii=False)
    return Response(movie_result)
