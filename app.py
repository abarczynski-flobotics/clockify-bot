import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, request
from slackeventsapi import SlackEventAdapter
import ast
import clockify_api
#import requests

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

@app.route('/add-project', methods=['POST'])
def add_project():
    data = request.form
    channel_id = data.get('channel_id')
    parameter = data.get('text')
    if parameter.lower().strip() == 'help':
        message = """
        Command: add-project
        Description: Adds new project to workspace.
        Parameter example:
        {
            "name": "My API Project",
            // OPTIONAL
            "clientId": "",
            "isPublic": "false",
            "color": "#f44336",
            "note": "This is project's note",
            "billable": "true",
            "public": false
        }"""
    else:
        try:
            body = ast.literal_eval(parameter.replace('\n', ''))
            message = clockify_api.add_project(body)
        except:
            message = 'Command parameter is not a json.'

    client.chat_postMessage(channel=channel_id, text=message)
    return Response(), 200

@app.route('/add-client', methods=['POST'])
def add_client():
    data = request.form
    channel_id = data.get('channel_id')
    parameter = data.get('text')
    if parameter.lower().strip() == 'help':
        message = """
        Command: add-client
        Description: Adds new client to workspace.
        Parameter example:
        {
            "name": "Client X",
            "note": "My note about Client X"
        }"""
    else:
        try:
            body = ast.literal_eval(parameter.replace('\n', ''))
            message = clockify_api.add_client(body)
        except:
            message = 'Command parameter is not a json.'

    client.chat_postMessage(channel=channel_id, text=message)
    return Response(), 200

@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.form
    channel_id = data.get('channel_id')
    parameter = data.get('text')
    if parameter.lower().strip() == 'help':
        message = """
        Command: add-user
        Description: Adds new user to workspace.
        Parameter example:
        {
            "email": "example@email.com"
        }"""
    else:
        try:
            body = ast.literal_eval(parameter.replace('\n', ''))
            message = clockify_api.add_client(body)
        except:
            message = 'Command parameter is not a json.'

    client.chat_postMessage(channel=channel_id, text=message)
    return Response(), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

