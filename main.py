#supabase tennis_scoreboard_data password: 00v2LrrgBdhsc0pD
#API Documentation: http://127.0.0.1:8000/docs

#populate match_data and then create a column in scoreboard_data_v2 that has a game ID base on match_data. purpose: to access data for a particular match
#get front end to populate match_data somehow.
#create a redo button. Similar to undo button. Maybe track a row as deleted or not deleted. at the end of the match, just delete the rows with deleted == True.

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
    response = supabase.table('scoreboard_data_v2').select('id').execute()

    id = 0
    if len(response.data) != 0:
        id = response.data[-1]['id'] + 1

    logging.info("Received data: %s", scoreboardData)
    if scoreboardData['prev_sets'][0]:
        upsert_data = [
            {'id': id, 'points_1': str(scoreboardData['points'][0]), 'games_1' : scoreboardData['games'][0], 'curr_sets_1' : scoreboardData['sets'][0], 'prev_sets_1':str(scoreboardData['prev_sets'][0]), 'points_2': str(scoreboardData['points'][1]), 'games_2' : scoreboardData['games'][1], 'curr_sets_2' : scoreboardData['sets'][1], 'prev_sets_2':str(scoreboardData['prev_sets'][1])}
        ]
    else:
        upsert_data = [
            {'id': id, 'points_1': str(scoreboardData['points'][0]), 'games_1' : scoreboardData['games'][0], 'curr_sets_1' : scoreboardData['sets'][0],'prev_sets_2':str([]), 'points_2': str(scoreboardData['points'][1]), 'games_2' : scoreboardData['games'][1], 'curr_sets_2' : scoreboardData['sets'][1],'prev_sets_2':str([])}
        ]

    
    # Perform the upsert operation
    data, count = supabase.table('scoreboard_data_v2').upsert(upsert_data).execute()
    return scoreboardData

#gets player name information. Will usually only need to get at the beginning
@app.get("/player_names")
def my_name():
    response = supabase.table('scoreboard_data').select("player_name").execute()
    return response

@app.get("/undo_score")
def undoScore():
    lastId_response = supabase.table('scoreboard_data_v2').select("id").order("id", desc = True).limit(1).execute()
    if lastId_response.data[0]['id']:
           
        delete_row = supabase.table('scoreboard_data_v2').delete().eq('id', lastId_response.data[0]['id']).execute()

        response = supabase.table('scoreboard_data_v2').select("*").execute()
        return response.data[-1]
    return None

#gets other scoreboard info. Will need to get everytime you need to refresh
@app.get("/scoreboard_data")
def scoreboardData():
    response = supabase.table('scoreboard_data').select("*").execute()
    return response





