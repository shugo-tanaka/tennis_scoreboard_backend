#supabase tennis_scoreboard_data password: 00v2LrrgBdhsc0pD

from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_API_KEY")
supabase: Client = create_client(url, key)

response = supabase.table('scoreboard_data').select("*").execute()
data, count = supabase.table('scoreboard_data').upsert({'id': 1, 'points': 45}).execute()


app = FastAPI()

origins = [
    "http://localhost:3000",  # Add your React app's URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scoreboard_input")


@app.get("/scoreboard_data/player_names")
def my_name():
    players = ['Koji Tanaka', 'Masanori Tanaka']
    return players

@app.get("/scoreboard_data/prev_sets")
def prev_sets():
    prevSets = [[6,0],[6,0]]
    return prevSets

@app.get("/scoreboard_data/sets")
def sets():
    sets = [2,0]
    return sets

@app.get("/scoreboard_data/games")
def games():
    games = [5,5]
    return games

@app.get("/scoreboard_data/points")
def points():
    points = [15,15]
    return points

@app.get("/serve_data")
def serves():
    serve_data = []
    return serve_data




