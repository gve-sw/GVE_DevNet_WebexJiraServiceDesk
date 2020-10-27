""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

# Import Section
from flask import Flask, render_template, request
import datetime
import requests
import json
import os
from webex import create_webhooks, delete_webhooks_with_name, respond_to_message, respond_to_button_press
from webexteamssdk import WebexTeamsAPI, Webhook



# load all environment variables
MESSAGE_WEBHOOK_RESOURCE = "messages"
MESSAGE_WEBHOOK_EVENT = "created"
CARDS_WEBHOOK_RESOURCE = "attachmentActions"
CARDS_WEBHOOK_EVENT = "created"

# TODO:Change EXTERNAL_WEBHOOK_URL to the external server you want to receive from Webex Teams
EXTERNAL_WEBHOOK_URL = "https://example.com"

#Global variables
flask_app = Flask(__name__)

#Methods
#Returns location and time of accessing device
def getSystemTimeAndLocation():
    #request user ip
    userIPRequest = requests.get('https://get.geojs.io/v1/ip.json')
    userIP = userIPRequest.json()['ip'] 

    #request geo information based on ip
    geoRequestURL = 'https://get.geojs.io/v1/ip/geo/' + userIP + '.json'
    geoRequest = requests.get(geoRequestURL)
    geoData = geoRequest.json()

    #create info string
    location = geoData['country']
    timezone = geoData['timezone']
    current_time=datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    timeAndLocation = "System Information: {}, {} (Timezone: {})".format(location, current_time, timezone)
    
    return timeAndLocation


##Routes
@flask_app.route('/',methods=['GET'])
def index():
    try:
        #Page without error message and defined header links 
        return render_template('instructions.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation())
    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return ""

# Core bot functionality
# Webex will post to this server when a message is created for the bot
# or when a user clicks on an Action.Submit button in a card posted by this bot
# Your Webex Teams webhook should point to http://<serverip>:<port>/events
@flask_app.route("/events", methods=["POST"])
def webex_teams_webhook_events():
    """Respond to inbound webhook JSON HTTP POST from Webex Teams."""
    # Create a Webhook object from the JSON data
    webhook_obj = Webhook(request.json)

    # Handle a new message event
    if (webhook_obj.resource == MESSAGE_WEBHOOK_RESOURCE
            and webhook_obj.event == MESSAGE_WEBHOOK_EVENT):
        respond_to_message(webhook_obj)

    # Handle an Action.Submit button press event
    elif (webhook_obj.resource == CARDS_WEBHOOK_RESOURCE
          and webhook_obj.event == CARDS_WEBHOOK_EVENT):
        respond_to_button_press(webhook_obj)

    # Ignore anything else (which should never happen
    else:
        print(f"IGNORING UNEXPECTED WEBHOOK:\n{webhook_obj}")

    return "OK"
    
def main():
    webhook_url = EXTERNAL_WEBHOOK_URL
    # Delete preexisting webhooks created by this script
    delete_webhooks_with_name()

    
    create_webhooks(webhook_url)
    port = int(os.environ.get("PORT", 8000))
    try:
        # Start the Flask web server
        flask_app.run(host="0.0.0.0", port=port)

    finally:
        print("Cleaning up webhooks...")
        delete_webhooks_with_name()


if __name__ == "__main__":
    main()
