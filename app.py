from email.quoprimime import body_length
import os
from dotenv import load_dotenv
import clockify_api
from slack_bolt import App
import views
import prepare_json

env_path ='.env'
load_dotenv(dotenv_path=env_path)
app = App(
    token=os.environ.get("SLACK_TOKEN"),
    signing_secret=os.environ.get("SIGNING_SECRET")
)

@app.view("")
def handle_view_events(ack, body):

    create_actions = {
        "Add new client": (clockify_api.add_client, prepare_json.json_add_client),
        "Add new project": (clockify_api.add_project, prepare_json.json_add_project),
        "Add new user": (clockify_api.add_user, prepare_json.json_add_user)
    }

    update_actions = {
        "Update project": (clockify_api.update_project, prepare_json.json_update_project)
    }

    action = body['view']['title']['text']

    if action in create_actions:
        clockify_api_func, prepare_json_func = create_actions[action]
        message, success = clockify_api_func(prepare_json_func(body))
    elif action in update_actions:
        clockify_api_func, prepare_json_func = update_actions[action]
        body['projects'] = clockify_api.get_all_projects()
        message, success = clockify_api_func(prepare_json_func(body))

    view_result = views.view_result

    if success:
        view_result['title']['text'] = 'Success!'
    else:
        view_result['title']['text'] = 'Error!'
    
    view_result['blocks'][0]['text']['text'] = message
    
    ack(response_action="update", view=view_result)


@app.action("add-client")
def open_add_client_window(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view=views.view_add_client
    )

@app.action("add-project")
def open_add_project_window(ack, body, client):
    ack()
    clients = clockify_api.get_all_clients()
    view = views.view_add_project
    if clients:
        view['blocks'][1]['element']['options'] = [{
						"text": {
							"type": "plain_text",
							"text": cl['name'],
						},
						"value": cl['id']
					} for cl in clients]
    client.views_open(
        trigger_id=body["trigger_id"],
        view=view
    )

@app.action("update-project")
def open_update_project_window(ack, body, client):
    ack()
    projects = clockify_api.get_all_projects()
    view = views.view_update_project
    if projects:
        view['blocks'][0]['element']['options'] = [{
						"text": {
							"type": "plain_text",
							"text": p['name'],
						},
						"value": p['id']
					} for p in projects]
    client.views_open(
        trigger_id=body["trigger_id"],
        view=view
    )


@app.action("add-user")
def open_add_user_window(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view=views.view_add_user
    )

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        client.views_publish(
            user_id=event["user"],
            view=views.view_app_home
)
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

