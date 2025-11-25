# the request handler script
# created by: Zach

# script imports
import requests
import json
from dotenv import load_dotenv
import os
from enum import Enum

# loading enviroment vars
load_dotenv()
API_TOKEN = os.getenv('ROBOT_EVENTS_API_TOKEN')

# base url
BASE_URL = "https://www.robotevents.com/api/v2"

# endpoint Enum class, only used for basic api interactions
class EndpointType(Enum):
    ENDPOINT_TEAMS = "/teams"
    ENDPOINT_EVENTS = "/events"
    ENDPOINT_SEASONS = "/seasons"

# the request headers
HEADERS = {
    "accept": "application/json",
    "Authorization": f'Bearer {API_TOKEN}',
    "User-Agent": 'team-bot/1.0 (zachary.duriancik@gmail.com)'
}

# the request params
TEAM_PARAMS = {
    "program[]": [1],
    "registered": True,
    "number[]": []
}

TEAM_EVENT_PARAMS = {
    "id": 0,
    "season[]": []
}

SEASON_PARAMS = {
    "program[]": [1],
    "active": True
}

# speical request params
MATCH_PARAMS = {
    # default is zero
    "id": 0,
    "season[]": []
}

SKILLS_PARAMS = {
    #default is zero
    "id": 0,
    "season[]": []
}

# test request function
#TODO: make function useable by bot after testing is complete

# getting response from api
def get_rb_events_data(endpointType, params=None):

    url = f'{BASE_URL}{endpointType}'

    # actually getting a response
    try:
        reponse = requests.get(url, headers=HEADERS, params=params)

        # Raise an expectation for bad status codes (4xx or 5xx)
        reponse.raise_for_status()

        print(f"Satus Code {reponse.status_code}")
        return reponse.json()
    except requests.exceptions.RequestException as e:
        print(f"An Error occured {e}")
        return None
    
# helper functions
def get_current_season_id():
    # getting the current season using /season
    season_data = get_rb_events_data(EndpointType.ENDPOINT_SEASONS.value, SEASON_PARAMS)
    # checking to see if we have data
    if season_data:
        print(json.dumps(season_data, indent=4))
        print(f"Current season name: {season_data["data"][0]['name']}, season id: {season_data["data"][0]["id"]}")
        return season_data["data"][0]["id"]

def get_current_season_name():
    season_data = get_rb_events_data(EndpointType.ENDPOINT_SEASONS.value, SEASON_PARAMS)
    # checking to see if we have data
    if season_data:
        print(json.dumps(season_data, indent=4))
        return season_data["data"][0]["name"]

def get_team_id(team_number):
    # getting the team id from their number
    TEAM_PARAMS["number[]"] = [team_number]
    for param in TEAM_PARAMS.values():
        if param != None:
            print("All values are accounted for.")
        else:
            print("a param is empty.")
    
    info = get_rb_events_data(EndpointType.ENDPOINT_TEAMS.value, TEAM_PARAMS)
    
    if info:
        return info["data"][0]["id"]
    else:
        return None
    
#match record functons
def get_match_record_from_team(team):
    Record_Dictoinary = {
        "wins": 0,
        "losses": 0,
        "ties": 0
    }
    #getting the season id and team id
    season_id = get_current_season_id()
    team_id = get_team_id(team)

    #checking to see if we have ids
    if not season_id and team_id:
        print(f"season id: {season_id} or team id: {team_id} does not exists or is not an active season or resiterd team.")
        return None
    
    # setting param info
    MATCH_PARAMS["id"] = team_id
    MATCH_PARAMS["season[]"] = season_id
    
    # getting the rankings
    ranking_data = get_rb_events_data(f"/teams/{MATCH_PARAMS['id']}/rankings", MATCH_PARAMS)

    #checking to see if we have data
    if not ranking_data or "data" not in ranking_data:
        print("no data found")
        return None
    
    # record vars
    total_wins = 0
    total_losses = 0
    total_ties = 0

    # looping throught each final rank in event
    for event_ranking in ranking_data["data"]:
        total_wins += event_ranking.get("wins", 0)
        total_losses += event_ranking.get("losses", 0)
        total_ties += event_ranking.get("ties", 0)
    
    #returning the data
    Record_Dictoinary["wins"] = total_wins
    Record_Dictoinary["losses"] = total_losses
    Record_Dictoinary["ties"] = total_ties
    return Record_Dictoinary
    



#TODO: finish other commands and come back to add match statistics
# moudle functions
def get_team_from_number(team_number):
    # setting the number param
    TEAM_PARAMS["number[]"] = [team_number]
    #checking to see if all of the params are not empty
    for param in TEAM_PARAMS.values():
        if param != None:
            print("All values are accounted for.")
        else:
            print("a param is empty.")
    
    team_data = get_rb_events_data(EndpointType.ENDPOINT_TEAMS.value, TEAM_PARAMS)
    if team_data:
        print(f"Team Data: {json.dumps(team_data, indent=4)}")
        record_data = get_match_record_from_team(team_number)
        return team_data, record_data

#TODO: make a specialized get function that deals with pages before using skills or awards commands
def get_team_skills(team_name):
    # setting the team id info
    team_info = get_team_from_number(team_name)
    if team_info:
        # getting skills
       SKILLS_PARAMS["id"] = get_team_id(team_name)
       if SKILLS_PARAMS["id"]:
           skills_data = get_rb_events_data(f"/teams/{SKILLS_PARAMS['id']}/skills", SKILLS_PARAMS)
           print(f"Team Data: {json.dumps(skills_data, indent=4)}")
           return skills_data


# team event function
def get_events_attended_by_team(team):
    # getting our season id first
    season_id = get_current_season_id()
    # then, we get our team id
    team_id = get_team_id(team)
    if season_id and team_id:
        TEAM_EVENT_PARAMS["id"] = team_id
        TEAM_EVENT_PARAMS["season[]"] = [season_id]
        events_data = get_rb_events_data(f"/teams/{TEAM_EVENT_PARAMS['id']}/events", TEAM_EVENT_PARAMS)
        if events_data:
            print(json.dumps(events_data, indent=4))
            events = events_data.get("data", [])
            return events






# example of usage
#event_data = get_rb_events_data(EndpointType.ENDPOINT_EVENTS.value, EVENT_PARAMS)

#if event_data:
    #print(json.dumps(event_data, indent=4))