def json_add_project(body):
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
    return json

def json_add_client(body):
    client_name = body['view']['state']['values']['client-name']['client-name']['value']
    client_note = body['view']['state']['values']['client-note']['client-note']['value']
    json = {
        "name": client_name,
        "note": client_note
    }
    return json

def json_add_user(body):
    user_email = body['view']['state']['values']['user-email']['user-email']['value']
    json = {
        "email": user_email
    }
    return json
