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

if __name__ == "__main__":
    app.run(debug=True)

