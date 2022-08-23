import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os

env_path = '.env'
load_dotenv(dotenv_path=env_path)

data = {'x-api-key': os.environ['API_KEY']}


def get_all_clients():
    url = f"https://api.clockify.me/api/v1/workspaces/{os.environ['WORKSPACE_ID']}/clients"
    r = requests.get(url, headers=data)
    return r.json()


def get_all_projects():
    url = f"https://api.clockify.me/api/v1/workspaces/{os.environ['WORKSPACE_ID']}/projects"
    r = requests.get(url, headers=data)
    return r.json()


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
        message = f'The project {res["name"]} has been added to workspace.'

    return message, r.ok

def update_project(*request_data):
    request_body = request_data[0][0]
    project_id = request_data[0][1]
    url = f"https://api.clockify.me/api/v1/workspaces/{os.environ['WORKSPACE_ID']}/projects/{project_id}"

    try:
        r = requests.put(url, headers=data, json=request_body)
        res = r.json()
        r.raise_for_status()
    except HTTPError as http_err:
        message = f'HTTP error occurred: {http_err}: {res["message"]}'
    except Exception as err:
        message = f'Other error occurred: {err}'  # Python 3.6
    else:
        message = f'The project {res["name"]} has been updated in workspace.'

    return message, r.ok






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
        message = f'The client {res["name"]} has been added to workspace.'

    return message, r.ok

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
        message = f'The user {request_body["email"]} has been added to workspace. Invitation sent to the user.'

    return message, r.ok