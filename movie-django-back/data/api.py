import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

class Tmdb_API:
    key = os.getenv("TMDB_KEY")
    url = 'https://api.themoviedb.org/3/movie/'
    
    def __init__(self, id):
        self.id = id
        self.query = f"{Tmdb_API.url}{self.id}?api_key={Tmdb_API.key}&language=ko-KR"