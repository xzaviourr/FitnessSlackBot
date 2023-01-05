import os
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

import sys
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from database.dba import connect_to_db
import yaml

with open(ROOT_DIR + '/database/db_queries.yaml') as stream:  # Load all the database Queries
    try:
        db_queries = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise Exception(exc)
    except FileNotFoundError as e:
        raise Exception(e)

conn = connect_to_db()
cursor = conn.cursor()
cursor.execute(db_queries['CREATE_CHALLENGE_TABLE'])
cursor.execute(db_queries['CREATE_CHALLENGE_COMPLETED_LOGS_TABLE'])
conn.commit()
conn.close()
