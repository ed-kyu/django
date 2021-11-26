import requests, json
from tqdm import tqdm
from api import Tmdb_API
import random

WHAT_WE_NEED = {
    "title", "poster_path", "overview", "popularity",
    "vote_average", "release_date", "runtime", "genres",
}

with open('./genre_new.json', 'r') as JSON:
    genre_list = json.load(JSON)
with open('./movie_new.json', 'r') as JSON:
    movie_list = json.load(JSON)

check_duplicates = {movie["pk"] for movie in movie_list}
# print(check_duplicates)    
print(f"original count: {len(check_duplicates)}")
pick = random.sample(range(0, 1000000), 10000)

# movie_list = []
# genre_list = []
cnt = 0

for id in tqdm(pick):
    if id not in check_duplicates:
        query = Tmdb_API(id).query
        res = requests.get(query)

        if res.status_code == 200:
            movie = res.json()

            for key in WHAT_WE_NEED:
                if not movie[key]:
                    break
            else:
                if movie["release_date"] > "2019-01-01": 
                    cnt += 1
                    print(f"Filtered Data: {cnt}")
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

with open("genre_new_2.json", 'w') as JSON:
    json.dump(genre_list, JSON, ensure_ascii=False)
    
with open("movie_new_2.json", 'w') as JSON:
    json.dump(movie_list, JSON, ensure_ascii=False)

print(f"{len(movie_list)}개의 영화가 저장됐습니다.")
print(f"이거 맞나요? {len(movie_list)}-{cnt}={len(check_duplicates)}")