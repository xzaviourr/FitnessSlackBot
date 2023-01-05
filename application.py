import os
ROOT_DIR = os.path.realpath(os.path.dirname(__file__))

import sys
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    
from flask import Flask, request
from urllib.parse import parse_qs
import json
from datetime import datetime
import yaml
from logger.logger import apiLogger
from database.dba import connect_to_db

with open(ROOT_DIR + '/database/db_queries.yaml') as stream:  # Load all the database Queries
    try:
        db_queries = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise Exception(exc)
    except FileNotFoundError as e:
        raise Exception(e)

application = Flask(__name__)

@application.route('/', methods = ['GET'])
def show_homepage():
    return "Tenacity Move Web Server Active"

@application.route('/interactivity/', methods = ['POST'])
def user_interactive_action():
    """
    All user events like like button click, modals, or other interactive components
    trigger this event.
    """
    # Button click event 
    usr_input = parse_qs(request.get_data().decode())['payload'][0]
    usr_dict = json.loads(usr_input)
    if usr_dict['type'] == 'block_actions': # Button click
        event = {
            "user_id": usr_dict['user']['id'],
            "channel_id": usr_dict['channel']['id'],
            "action": usr_dict['actions'][0]['value'],
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        if event['action'] == "challenge_completed":
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(db_queries['INSERT_CHALLENGE_LOG']%(event['user_id'], event['channel_id'], event['user_id'], event['channel_id']))
            conn.commit()
            conn.close()

        apiLogger.info(json.dumps(event, indent=4))

    return "SUCCESS"

@application.route('/event/', methods = ['POST'])
def user_event_action():
    """
    All user events like new messages in the channel, reactions, files, etc 
    trigger this event. 
    """
    usr_input = json.loads(request.get_data().decode())
    if usr_input['type'] == 'url_verification':     # Verification of Event API by slack
        apiLogger.info("Event API Verified")
        return usr_input['challenge']
    
    if usr_input['type'] == 'event_callback':       # Events triggered from application
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if usr_input['event']['type'] == "app_mention":     # When bot is mentioned by any user
            user_id = usr_input['event']['user']
            channel = usr_input['event']['channel']
            message = usr_input['event']['text']

        elif usr_input['event']['type'] == "message":       # When new message is posted in the channel
            user_id = usr_input['event']['user']
            channel = usr_input['event']['channel']
            message = usr_input['event']['text']

        elif usr_input['event']['type'] == "reaction_added":    # When user reacts on any message
            user_id = usr_input['event']['user']
            reaction = usr_input['event']['reaction']
            channel_id = usr_input['event']['item']['channel']

            if reaction == "white_check_mark":
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute(db_queries['INSERT_CHALLENGE_LOG']%(user_id, channel_id, user_id, channel_id))
                conn.commit()
                conn.close()

    return "SUCCESS"

if __name__ == "__main__":
    application.run(debug=True, port=8080)