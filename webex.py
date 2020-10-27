from webexteamssdk import WebexTeamsAPI, Webhook
import os
from urllib.parse import urljoin
import json
from jira import create_request

WEBHOOK_NAME = "ACI Ticket Bot"
WEBHOOK_URL_SUFFIX = "/events"
MESSAGE_WEBHOOK_RESOURCE = "messages"
MESSAGE_WEBHOOK_EVENT = "created"
CARDS_WEBHOOK_RESOURCE = "attachmentActions"
CARDS_WEBHOOK_EVENT = "created"
# TODO: Update the WEBEX_TEAMS_ACCESS_TOKEN with your Bot's webex teams bearer token.
WEBEX_TEAMS_ACCESS_TOKEN = "REPLACE WITH BOT BEARER TOKEN"


api = WebexTeamsAPI(WEBEX_TEAMS_ACCESS_TOKEN)
bot = api.people.me()





def get_json_card(filepath):
	with open(filepath, 'r') as f:
		json_card = json.loads(f.read())
		print(json_card)

		f.close()

	return json_card


def delete_webhooks_with_name():
    """List all webhooks and delete webhooks created by this script."""
    for webhook in api.webhooks.list():
        if webhook.name == WEBHOOK_NAME:
            print("Deleting Webhook:", webhook.name, webhook.targetUrl)
            api.webhooks.delete(webhook.id)


def create_webhooks(webhook_url):
    """Create the Webex Teams webhooks we need for our bot."""
    print("Creating Message Created Webhook...")
    webhook = api.webhooks.create(
        resource=MESSAGE_WEBHOOK_RESOURCE,
        event=MESSAGE_WEBHOOK_EVENT,
        name=WEBHOOK_NAME,
        targetUrl=urljoin(webhook_url, WEBHOOK_URL_SUFFIX)
    )
    print(webhook)
    print("Webhook successfully created.")

    print("Creating Attachment Actions Webhook...")
    webhook = api.webhooks.create(
        resource=CARDS_WEBHOOK_RESOURCE,
        event=CARDS_WEBHOOK_EVENT,
        name=WEBHOOK_NAME,
        targetUrl=urljoin(webhook_url, WEBHOOK_URL_SUFFIX)
    )
    print(webhook)
    print("Webhook successfully created.")


def respond_to_button_press(webhook):
    """Respond to a button press on the card we posted"""

    # Some server side debugging
    room = api.rooms.get(webhook.data.roomId)
    attachment_action = api.attachment_actions.get(webhook.data.id)
    person = api.people.get(attachment_action.personId)
    message_id = attachment_action.messageId
    
    data = json.loads(attachment_action.to_json())
    


    service_desk_response = create_request({"summary": data['inputs']['summary'], "description": data['inputs']['description']}, data['inputs']['raisedFor'])
    print(service_desk_response)
    print(data['inputs'])
    
    print(
        f"""
        NEW BUTTON PRESS IN ROOM '{room.title}'
        FROM '{person.displayName}'
        """
    )

    api.messages.create(
        room.id,
        parentId=message_id,
        markdown= ("Your ticket has been submitted to the support team! You can view your ticket [HERE](%s)"%service_desk_response['_links']['web']+
                  "\n>Ticket details:\n**Issue Key**: %s\n**%s**: %s\n**%s**: %s")%(service_desk_response['issueKey'],service_desk_response['requestFieldValues'][0]['label'],service_desk_response['requestFieldValues'][0]['value'],service_desk_response['requestFieldValues'][1]['label'],service_desk_response['requestFieldValues'][1]['value'])
    )

    api.messages.delete(message_id)


def respond_to_message(webhook):
    """Respond to a message to our bot"""

    # Some server side debugging
    room = api.rooms.get(webhook.data.roomId)
    message = api.messages.get(webhook.data.id)
    person = api.people.get(message.personId)
    print(
        f"""
        NEW MESSAGE IN ROOM '{room.title}'
        FROM '{person.displayName}'
        MESSAGE '{message.text}'
        """
    )

    # This is a VERY IMPORTANT loop prevention control step.
    # If you respond to all messages...  You will respond to the messages
    # that the bot posts and thereby create a loop condition.
    if message.personId == bot.id:
        # Message was sent by me (bot); do not respond.
        return "OK"

    else:
        # Message was sent by someone else; parse message and respond.
        api.messages.create(
            room.id,
            text="Thanks for contacting support, please fill out the General Service Request below!",
        )
        api.messages.create(
            room.id,
            text="If you see this your client cannot render cards",
            attachments=[{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": get_json_card("gsrCard.json")
            }],
        )
        return "OK"
