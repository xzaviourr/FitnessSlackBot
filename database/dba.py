import os
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

import sys
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import psycopg2
import json

def connect_to_db():
    """
    Create a connection object with the postgres database.
    return: connection object
    """
    try:
        with open(ROOT_DIR + "/config/db_credentials.json") as file:    # Load database credentials from the config file
            credentials = json.load(file)
    except FileNotFoundError as e:
        raise Exception(e)
            
    try:
        conn = psycopg2.connect(
            host = credentials['host'],
            port = credentials['port'],
            database = credentials['database'],
            user = credentials['user'],
            password = credentials['password']
        )
        return conn
    except Exception as e:
        raise Exception(e)