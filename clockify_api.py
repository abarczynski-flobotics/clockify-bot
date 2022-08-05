import requests
from requests.exceptions import HTTPError
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

data = {'x-api-key': os.environ['API_KEY']}

def add_project(request_body):

    url = f"https://api.clockify.me/api/v1/workspaces/{os.environ['WORKSPACE_ID']}/projects"
    
    try:
        r = requests.post(url, headers=data, json=request_body)
        res = r.json()
        r.raise_for_status()
    except HTTPError as http_err:
        message = f'HTTP error occurred: {http_err}: {res["message"]}'
    except Exception as err:
        message = f'Other error occurred: {err}'  # Python 3.6
    else:
        message = f'Success! The project {res["name"]} with id {res["id"]} has been added to workspace.'

    return message

def add_client(request_body):

    url = f"https://api.clockify.me/api/v1/workspaces/{os.environ['WORKSPACE_ID']}/clients"

    try:
        r = requests.post(url, headers=data, json=request_body)
        res = r.json()
        r.raise_for_status()
    except HTTPError as http_err:
        message = f'HTTP error occurred: {http_err}: {res["message"]}'
    except Exception as err:
        message = f'Other error occurred: {err}'  # Python 3.6
    else:
        message = f'Success! The client {res["name"]} with id {res["id"]} has been added to workspace.'

    return message

def add_user(request_body):

    url = f"https://api.clockify.me/api/v1/workspaces/{os.environ['WORKSPACE_ID']}/users"

    try:
        r = requests.post(url, headers=data, json=request_body)
        res = r.json()
        r.raise_for_status()
    except HTTPError as http_err:
        message = f'HTTP error occurred: {http_err}: {res["message"]}'
    except Exception as err:
        message = f'Other error occurred: {err}'  # Python 3.6
    else:
        message = f'Success! The user {request_body["email"]} has been added to workspace.'

    return message