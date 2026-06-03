import requests
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

app = FastAPI()

BASE_DIR = Path(__file__).parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
def serve_home():
    return FileResponse(str(FRONTEND_DIR / "main.html"))

@app.get("/detail")
def serve_detail():
    return FileResponse(str(FRONTEND_DIR / "detail.html"))

def get_movie_data(movie_input):
    base_url = "http://www.omdbapi.com/"
    movie_name = f"?s={movie_input}"
    api_key = f"&apikey={OMDB_API_KEY}"
    url = f"{base_url}{movie_name}{api_key}"

    response = requests.get(url)

    data = response.json()

    if data.get("Response") == "False":
        return []

    movie_list = data["Search"]
    total_movies = []

    for movie in movie_list:
        movie_title = movie["Title"]
        movie_year = movie["Year"]
        movie_poster = movie["Poster"]
        movie_id = movie["imdbID"]

        single_movie = {
            "title" : movie_title,
            "year" : movie_year,
            "poster" : movie_poster,
            "imdbID" : movie_id
        }
        total_movies.append(single_movie)

    return total_movies

@app.get("/search")
def search_movie(movie: str):
    return get_movie_data(movie)

def get_fullMovie_data(movie_input):
    base_url = "http://www.omdbapi.com/"
    movie_id = f"?i={movie_input}"
    api_key = f"&apikey={OMDB_API_KEY}"
    url = f"{base_url}{movie_id}{api_key}"

    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "False":
        return {}

    return data

@app.get("/movie/{imdbID}")
def get_movie(imdbID: str):
    return get_fullMovie_data(imdbID)

