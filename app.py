import os
from dotenv import load_dotenv
import clockify_api
from slack_bolt import App
import views

env_path ='.env'
load_dotenv(dotenv_path=env_path)
app = App(
    token=os.environ.get("SLACK_TOKEN"),
    signing_secret=os.environ.get("SIGNING_SECRET")
)



def get_value(field, body):
    return [v for k,v in body['view']['state']['values'].items() if field in v][0][field]['value']


@app.view("")
def handle_view_events(ack, body):
    if body['view']['title']['text'] == "Add new client":
        client_name = body['view']['state']['values']['client-name']['client-name']['value']
        client_note = body['view']['state']['values']['client-note']['client-note']['value']
        json = {
            "name": client_name,
            "note": client_note
        }
        message, success = clockify_api.add_client(json)
    elif body['view']['title']['text'] == "Add new project":
        project_name = body['view']['state']['values']['project-name']['project-name']['value']
        client_id = body['view']['state']['values']['client-name']['client-name']['selected_option']['value']
        project_note = body['view']['state']['values']['project-note']['project-note']['value']
        billable = bool(len(body['view']['state']['values']['billable']['billable']['selected_options']))
        public = bool(len(body['view']['state']['values']['public']['public']['selected_options']))
        json = {
            "name": project_name,
            "clientId": client_id if client_id != 'value-0' else None,
            "note": project_note,
            "billable": billable,
            "isPublic": public
        }
        message, success = clockify_api.add_project(json)
    elif body['view']['title']['text'] == "Add new user":
        user_email = body['view']['state']['values']['user-email']['user-email']['value']
        json = {
            "email": user_email
        }
        message, success = clockify_api.add_user(json)

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
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id=event["user"],
            # the view object that appears in the app home
            view=views.view_app_home
)
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

