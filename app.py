import os
from dotenv import load_dotenv
import clockify_api as clockify_api
from slack_bolt import App
import views as views
import prepare_json as prepare_json
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_bolt.authorization import authorize
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

env_path = '.env'
load_dotenv(dotenv_path=env_path)

# oauth_settings = OAuthSettings(
#     client_id=os.environ["SLACK_CLIENT_ID"],
#     client_secret=os.environ["SLACK_CLIENT_SECRET"],
#     scopes=["channels:history", "channels:read", "chat:write", "groups:history",
#             "groups:read", "groups:write", "users:read", "im:history"],
#     installation_store=FileInstallationStore(base_dir="./data/installations"),
#     state_store=FileOAuthStateStore(
#         expiration_seconds=600, base_dir="./data/states"),
#     install_page_rendering_enabled=False
# )

app = App(
    token=os.environ.get('SLACK_TOKEN'),
    signing_secret=os.environ.get('SIGNING_SECRET'),
    # oauth_settings=oauth_settings,
    process_before_response=True
)


@app.view('')
def handle_view_events(ack, body):

    create_actions = {
        'Add new client': (clockify_api.add_client, prepare_json.json_add_client),
        'Add new project': (clockify_api.add_project, prepare_json.json_add_project),
        'Add new user': (clockify_api.add_user, prepare_json.json_add_user)
    }

    update_actions = {
        'Update project': (clockify_api.update_project, prepare_json.json_update_project)
    }

    action = body['view']['title']['text']

    if action in create_actions:
        clockify_api_func, prepare_json_func = create_actions[action]
        message, success = clockify_api_func(prepare_json_func(body))
    elif action in update_actions:
        clockify_api_func, prepare_json_func = update_actions[action]
        body['projects'] = clockify_api.get_all_projects()
        message, success = clockify_api_func(prepare_json_func(body))

    view_result = views.view_result()

    if success:
        view_result['title']['text'] = 'Success!'
    else:
        view_result['title']['text'] = 'Error!'

    view_result['blocks'][0]['text']['text'] = message

    ack(response_action='update', view=view_result)


@app.action('add-client')
def open_add_client_window(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body['trigger_id'],
        view=views.view_add_client()
    )


@app.action('add-project')
def open_add_project_window(ack, body, client):
    ack()
    clients = [cl for cl in clockify_api.get_all_clients()
               if not cl['archived']]
    view = views.view_add_project()
    if clients:
        view['blocks'][1]['element']['options'] = [{
            'text': {
                'type': 'plain_text',
                'text': cl['name'],
            },
            'value': cl['id']
        } for cl in clients]
    client.views_open(
        trigger_id=body['trigger_id'],
        view=view
    )


@app.action('update-project')
def open_update_project_window(ack, body, client):
    ack()
    projects = [p for p in clockify_api.get_all_projects()
                if not p['archived']]
    view = views.view_update_project()
    if projects:
        view['blocks'][0]['element']['options'] = [{
            'text': {
                'type': 'plain_text',
                'text': p['name'],
            },
            'value': p['id'] + ' - ' + str(projects.index(p))
        } for i, p in enumerate(projects[0:min(100, len(projects))])]
        if len(projects) > 100:
            view['blocks'].insert(1, {
                'type': 'actions',
                'elements': [
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': 'Show next projects'
                        },
                        'style': 'primary',
                        'value': 'click_me_123',
                        'action_id': 'show-next-proj'
                    }
                ]
            })

    client.views_open(
        trigger_id=body['trigger_id'],
        view=view
    )


@app.action('show-next-proj')
def update_update_project_window(ack, body, client):
    ack()
    projects = [p for p in clockify_api.get_all_projects()
                if not p['archived']]
    view = views.view_update_project()
    if projects:
        current_min_index = int(
            body['view']['blocks'][0]['element']['options'][0]['value'].split(' - ')[-1])
        current_max_index = int(
            body['view']['blocks'][0]['element']['options'][-1]['value'].split(' - ')[-1])
        next_min_index = current_min_index + 100
        next_max_index = min(current_max_index + 100, len(projects))

        if next_max_index < len(projects):
            view['blocks'].insert(1, {
                'type': 'actions',
                'elements': [{
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Show previous projects'
                    },
                    'style': 'danger',
                    'value': 'click_me_123',
                    'action_id': 'show-prev-proj'
                }, {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Show next projects'
                    },
                    'style': 'primary',
                    'value': 'click_me_123',
                    'action_id': 'show-next-proj'
                }
                ]
            })
        else:
            view['blocks'].insert(1, {
                'type': 'actions',
                'elements': [{
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Show previous projects'
                    },
                    'style': 'danger',
                    'value': 'click_me_123',
                    'action_id': 'show-prev-proj'
                }
                ]
            })

        view['blocks'][0]['element']['options'] = [{
            'text': {
                'type': 'plain_text',
                'text': p['name'],
            },
            'value': p['id'] + ' - ' + str(projects.index(p))
        } for i, p in enumerate(projects[next_min_index:next_max_index+1])]

    client.views_update(
        view_id=body['view']['id'],
        hash=body['view']['hash'],
        view=view
    )


@app.action('show-prev-proj')
def update_update_project_window(ack, body, client):
    ack()
    projects = [p for p in clockify_api.get_all_projects()
                if not p['archived']]
    view = views.view_update_project()
    if projects:
        current_min_index = int(
            body['view']['blocks'][0]['element']['options'][0]['value'].split(' - ')[-1])
        next_min_index = max(current_min_index - 100, 0)
        next_max_index = current_min_index - 1

        if next_min_index > 0:
            view['blocks'].insert(1, {
                'type': 'actions',
                'elements': [{
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Show previous projects'
                    },
                    'style': 'danger',
                    'value': 'click_me_123',
                    'action_id': 'show-prev-proj'
                }, {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Show next projects'
                    },
                    'style': 'primary',
                    'value': 'click_me_123',
                    'action_id': 'show-next-proj'
                }
                ]
            })
        else:
            view['blocks'].insert(1, {
                'type': 'actions',
                'elements': [{
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Show next projects'
                    },
                    'style': 'primary',
                    'value': 'click_me_123',
                    'action_id': 'show-next-proj'
                }
                ]
            })

        view['blocks'][0]['element']['options'] = [{
            'text': {
                'type': 'plain_text',
                'text': p['name'],
            },
            'value': p['id'] + ' - ' + str(projects.index(p))
        } for i, p in enumerate(projects[next_min_index:next_max_index+1])]

    client.views_update(
        view_id=body['view']['id'],
        hash=body['view']['hash'],
        view=view
    )


@app.action('add-user')
def open_add_user_window(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body['trigger_id'],
        view=views.view_add_user()
    )


@app.message("start")
def say_hello(client, message, say):
    channel_id = message['channel']
    if channel_id == 'C03VATR9BPD':
        say(
            blocks=views.clockify_buttons(),
            text="Select action"
        )


SlackRequestHandler.clear_all_log_handlers()


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
