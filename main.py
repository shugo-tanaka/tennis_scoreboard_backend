#supabase tennis_scoreboard_data password: 00v2LrrgBdhsc0pD
#API Documentation: http://127.0.0.1:8000/docs
# when match info gets updated, update previous logs. 
# when I click the points too fast, supabase doesn't update properly. 


from typing import Union, List, Dict, Any
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
host_link: str = os.environ.get("FRONTEND_URL")
supabase: Client = create_client(url, key)

print(host_link)

app = FastAPI()

origins = [
    host_link,  # Add your React app's URL here
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

@app.post("/match_data")
def matchData(matchData: dict):
    logging.info("Received data: %s", matchData)
    delete_row = supabase.table('match_data').delete().execute()
    upsert_data = [{'date': matchData['date'],  'player_1':matchData['player1Name'], 'player_2':matchData['player2Name']}]
    data,count = supabase.table('match_data').upsert(upsert_data).execute()
    return matchData

@app.post("/serve_locations")
def serveLocations(serveLoc: dict):
    logging.info("Received data: %s", serveLoc)
    
    if serveLoc['sX']:
        x = serveLoc['sX']
        y = serveLoc['sY']
        ballText = serveLoc['sBallText']
    else:
        x = []
        y = []
        ballText = []
    upsert_data_serve = [{'x':x, 'y':y, 'ball_text':ballText}]
    data,count = supabase.table('serve_locations').upsert(upsert_data_serve).execute()
    return serveLoc

@app.post("/scoreboard_input")
def scoreboardInput(scoreboardData: dict):
    # Log the received data
    response = supabase.table('scoreboard_data_v2').select('id').execute()
    

    id = 0
    if len(response.data) != 0:
        x = response.data
        x.sort(key = lambda x: x['id'])
        id = x[-1]['id'] + 1

    logging.info("Received data: %s", scoreboardData)
    if scoreboardData['prev_sets'][0]:
        upsert_data = [
            {'id': id, 'points_1': str(scoreboardData['points'][0]), 'games_1' : scoreboardData['games'][0], 'curr_sets_1' : scoreboardData['sets'][0], 'prev_sets_1':scoreboardData['prev_sets'][0], 'points_2': str(scoreboardData['points'][1]), 'games_2' : scoreboardData['games'][1], 'curr_sets_2' : scoreboardData['sets'][1], 'prev_sets_2':scoreboardData['prev_sets'][1], 'player1':scoreboardData['player_name'][0], 'player2':scoreboardData['player_name'][1],'date': scoreboardData['date'], 'server': scoreboardData['selectedServer']}
        ]
    else:
        upsert_data = [
            {'id': id, 'points_1': str(scoreboardData['points'][0]), 'games_1' : scoreboardData['games'][0], 'curr_sets_1' : scoreboardData['sets'][0],'prev_sets_1':[], 'points_2': str(scoreboardData['points'][1]), 'games_2' : scoreboardData['games'][1], 'curr_sets_2' : scoreboardData['sets'][1],'prev_sets_2':[], 'player1':scoreboardData['player_name'][0], 'player2':scoreboardData['player_name'][1],'date': scoreboardData['date'], 'server': scoreboardData['selectedServer']}
        ]

    
    # Perform the upsert operation
    data, count = supabase.table('scoreboard_data_v2').upsert(upsert_data).execute()
    return scoreboardData

#gets player name information. Will usually only need to get at the beginning
@app.get("/player_names")
def my_name():
    response = supabase.table('match_data').select("*").execute()
    return [response.data[-1]['player_1'], response.data[-1]['player_2']]

@app.get("/undo_score")
def undoScore():
    lastId_response = supabase.table('scoreboard_data_v2').select("id").order("id", desc = True).limit(1).execute()
    if lastId_response.data[0]['id']:
           
        delete_row = supabase.table('scoreboard_data_v2').delete().eq('id', lastId_response.data[0]['id']).execute()

        response = supabase.table('scoreboard_data_v2').select('*').execute()
        return response
    return None

#gets other scoreboard info. Will need to get everytime you need to refresh
@app.get("/scoreboard_data")
def scoreboardData():
    response = supabase.table('scoreboard_data_v2').select("*").execute()
    x = response.data
    x.sort(key = lambda i: i['id'])
    # print(x[-1])
    return x[-1]

#get serveCircleData for frontend
@app.get("/serve_circles")
def servCircles():
    response = supabase.table('serve_locations').select("*").execute()
    
    if len(response.data) > 0:
        logging.info("About to send data: %s", response.data[-1])
        return response.data[-1]
    return None





