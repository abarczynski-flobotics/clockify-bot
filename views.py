view_add_project={
	"type": "modal",
	"title": {
		"type": "plain_text",
		"text": "Add new project"
	},
	"submit": {
		"type": "plain_text",
		"text": "Create"
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel"
	},
	"blocks": [
		{
			"type": "input",
			"block_id": "project-name",
			"element": {
				"type": "plain_text_input",
				"action_id": "project-name"
			},
			"label": {
				"type": "plain_text",
				"text": "Project Name"
			}
		},
		{
			"type": "input",
			"block_id": "client-name",
			"optional": True,
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select client name"
				},
				"options": [{
						"text": {
							"type": "plain_text",
							"text": " "
						},
						"value": "value-0"
					}
				],
				"action_id": "client-name"
			},
			"label": {
				"type": "plain_text",
				"text": "Client Name"
			}
		},
		{
			"type": "input",
			"block_id": "project-note",
			"optional": True,
			"element": {
				"type": "plain_text_input",
				"action_id": "project-note"
			},
			"label": {
				"type": "plain_text",
				"text": "Project Note"
			}
		},
		{
			"type": "input",
			"block_id": "billable",
			"optional": True,
			"element": {
				"type": "checkboxes",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": " "
						},
						"value": "value-0"
					}
				],
				"action_id": "billable"
			},
			"label": {
				"type": "plain_text",
				"text": "Billable"
			}
		},
		{
			"type": "input",
			"block_id": "public",
			"optional": True,
			"element": {
				"type": "checkboxes",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": " "
						},
						"value": "value-0"
					}
				],
				"action_id": "public"
			},
			"label": {
				"type": "plain_text",
				"text": "Public"
			}
		}
	]
}


view_update_project = {
	"type": "modal",
	"title": {
		"type": "plain_text",
		"text": "Update project"
	},
	"submit": {
		"type": "plain_text",
		"text": "Update"
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel"
	},
	"blocks": [
		{
			"type": "input",
			"block_id": "project-name",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select project name"
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": " "
						},
						"value": "value-0"
					}
				],
				"action_id": "project-name"
			},
			"label": {
				"type": "plain_text",
				"text": "Project Name"
			}
		},
		{
			"type": "input",
			"block_id": "hourly-rate",
			"element": {
				"type": "plain_text_input",
				"action_id": "hourly-rate"
			},
			"label": {
				"type": "plain_text",
				"text": "Hourly Rate"
			}
		}
	]
}

view_add_client = {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "Add new client",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Create",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "client-name",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "client-name"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Client Name",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "optional": True,
                    "block_id": "client-note",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "client-note"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Note",
                        "emoji": True
                    }
                }
            ]
        }

view_add_user = {
	"type": "modal",
	"title": {
		"type": "plain_text",
		"text": "Add new user"
	},
	"submit": {
		"type": "plain_text",
		"text": "Create"
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel"
	},
	"blocks": [
		{
			"type": "input",
			"block_id": "user-email",
			"element": {
				"type": "plain_text_input",
				"action_id": "user-email"
			},
			"label": {
				"type": "plain_text",
				"text": "User Email"
			}
		}
	]
}



view_result = {
	"type": "modal",
	"title": {
		"type": "plain_text",
		"text": "{}"
	},
    "close": {
		"type": "plain_text",
		"text": "Close"
	},
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "{}",
				"emoji": True
			}
		}
	]
}

view_app_home = {
	"type": "home",
	"blocks": [
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Add new client"
					},
					"value": "click_me_123",
					"action_id": "add-client"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Add new project"
					},
					"value": "click_me_123",
					"action_id": "add-project"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Update project"
					},
					"value": "click_me_123",
					"action_id": "update-project"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Add new user"
					},
					"value": "click_me_123",
					"action_id": "add-user"
				}
			]
		}
	]
}