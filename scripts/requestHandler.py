# the request handler script

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

# the request headers
HEADERS = {
    "accept": "application/json",
    "Authorization": f'Bearer {API_TOKEN}',
    "User-Agent": 'team-bot/1.0 (zachary.duriancik@gmail.com)'
}

# the request params
TEAM_PARAMS = {
    "program[]": [1],
    "region": "Virgina",
    "registered": True,
    "number[]": []
}

EVENT_PARAMS = {
    "program[]": [1],
    "evenTypes[]": ["tornament", "league"] 
}

# speical request params
MATCH_PARAMS = {
    # default is zero
    "id": 0,
    "season[]": [180]
}

SKILLS_PARAMS = {
    #default is zero
    "id": 0,
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
        return team_data

#TODO: make a specialized get function that deals with pages before using skills or awards commands
def get_team_skills(team_name):
    # setting the team id info
    team_info = get_team_from_number(team_name)
    if team_info:
        # getting skills
       SKILLS_PARAMS["id"] = team_info['data'][0]["id"]
       if SKILLS_PARAMS["id"]:
           skills_data = get_rb_events_data(f"/teams/{SKILLS_PARAMS['id']}/skills", SKILLS_PARAMS)
           print(f"Team Data: {json.dumps(skills_data, indent=4)}")
           return skills_data

# event function
def get_event_by_name(event_name):
    # getting data from "/events" request
    event_info = get_rb_events_data(EndpointType.ENDPOINT_EVENTS.value, EVENT_PARAMS)
    #checking for event info
    if event_info:
        # getting event name
        print(f"event data: {json.dumps(event_info, indent=4)}")
        for event in event_info:
            for key, value in event.items():
                if key == "name" and value == event_name:
                    print("event name found!")
    


# example of usage
#event_data = get_rb_events_data(EndpointType.ENDPOINT_EVENTS.value, EVENT_PARAMS)

#if event_data:
    #print(json.dumps(event_data, indent=4))