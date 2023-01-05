import os
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

import sys
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import json
from slack_sdk import WebClient
import yaml

from database.dba import connect_to_db

class Message:
    """
    Base class for all the messages that will be sent on slack. This includes personal dm's, cron job messages,
    and everything else. 
    """
    def __init__(self):
        try:
            with open(ROOT_DIR + "/config/credentials.json", 'r') as file:    # Load Slack BOT configurations
                self.credentials = json.load(file)
        except FileNotFoundError as e:
            raise Exception(e)

        with open(ROOT_DIR + '/database/db_queries.yaml') as stream:  # Load all the database Queries
            try:
                self.db_queries = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise Exception(exc)
            except FileNotFoundError as e:
                raise Exception(e)

        self.client = WebClient(token=self.credentials['bot_oauth_token'])  # Client for slack communications
        self.db_conn = connect_to_db()  # Establish connection with the database

        self.channel_id_mapping = {
            "bot_testing": "C03D2NCT06R"
        }