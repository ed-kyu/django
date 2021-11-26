import requests, json
from tqdm import tqdm
from api import Tmdb_API
import random

pick = random.sample(range(0, 760000), 1)

movie_list = []
genre_list = []

for id in tqdm(pick):
    query = Tmdb_API(id).query
    res = requests.get(query)

    if res.status_code == 200:
        movie = res.json()
        for key in movie:
            if not movie[key]:
                print(f"{key}: {movie[key]}")
        else: 
            genres = movie.get('genres')
            for genre in genres:
                genre_dict = {
                    "model": "movies.genre",
                    "pk": genre.get("id"),
                    "fields": {
                        "name": genre.get("name"),
                    }
                }
                genre_list.append(genre_dict)


            movie_dict = {
                "model": "movies.movie",
                "pk": movie["id"],
                "fields": {
                    "title": movie["title"], 
                    "poster_path": movie["poster_path"], 
                    "overview": movie["overview"], 
                    "popularity": movie["popularity"],
                    "vote_average": movie["vote_average"], 
                    "release_date": movie["release_date"], 
                    "runtime": movie["runtime"],
                    "genres": [i["id"] for i in genres],
                }
            }
            movie_list.append(movie_dict)

with open("genre.json", 'w') as JSON:
    json.dump(genre_list, JSON, ensure_ascii=False)
    
with open("movie.json", 'w') as JSON:
    json.dump(movie_list, JSON, ensure_ascii=False)

print(f"{len(movie_list)}개의 영화가 저장됐습니다.")