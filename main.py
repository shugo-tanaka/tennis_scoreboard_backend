#supabase tennis_scoreboard_data password: 00v2LrrgBdhsc0pD
#API Documentation: http://127.0.0.1:8000/docs

#To Do: frontend update is delayed. 

from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging
import numpy as np

load_dotenv()  # take environment variables from .env.

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_API_KEY")
supabase: Client = create_client(url, key)

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

@app.get("/test/")
def test():
    response = supabase.table('scoreboard_data').select("*").execute() #get data from Supabase
    data, count = supabase.table('scoreboard_data').upsert({'id': 1, 'points': 0}).execute() #update Supabase
    return response   

@app.post("/scoreboard_input")
def scoreboardInput(scoreboardData: dict):
    # Log the received data
    logging.info("Received data: %s", scoreboardData)
    if scoreboardData['prev_sets'][0]:
        upsert_data = [
            {'id': 0, 'points': str(scoreboardData['points'][0]), 'games' : scoreboardData['games'][0], 'sets' : scoreboardData['sets'][0], 'previous_sets':str(scoreboardData['prev_sets'][0])},
            {'id': 1, 'points': str(scoreboardData['points'][1]), 'games' : scoreboardData['games'][1], 'sets' : scoreboardData['sets'][1], 'previous_sets':str(scoreboardData['prev_sets'][1])}
        ]
    else:
        upsert_data = [
            {'id': 0, 'points': str(scoreboardData['points'][0]), 'games' : scoreboardData['games'][0], 'sets' : scoreboardData['sets'][0]},
            {'id': 1, 'points': str(scoreboardData['points'][1]), 'games' : scoreboardData['games'][1], 'sets' : scoreboardData['sets'][1]}
        ]

    
    # Perform the upsert operation
    data, count = supabase.table('scoreboard_data').upsert(upsert_data).execute()
    return scoreboardData

#gets player name information. Will usually only need to get at the beginning
@app.get("/player_names")
def my_name():
    response = supabase.table('scoreboard_data').select("player_name").execute()
    return response

#gets other scoreboard info. Will need to get everytime you need to refresh
@app.get("/scoreboard_data")
def scoreboardData():
    response = supabase.table('scoreboard_data').select("*").execute()
    return response





