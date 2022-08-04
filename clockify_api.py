import requests
from requests.exceptions import HTTPError
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

def add_project(request_body):

    url = f"https://api.clockify.me/api/v1/workspaces/{os.environ['WORKSPACE_ID']}/projects"
    data = {'x-api-key': os.environ['API_KEY']}

    try:
        r = requests.post(url, headers=data, json=request_body)
        r.raise_for_status()
    except HTTPError as http_err:
        message = print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        message = f'Other error occurred: {err}'  # Python 3.6
    else:
        message = f'Success! The project {request_body["name"]} has been created'

    return message

