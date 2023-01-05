import os
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

import sys
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from modules.message import Message
from logger.logger import messageLogger
from slack_sdk.errors import SlackApiError

class MorningChallenge(Message):
    def __init__(self):
        super().__init__()        

    def load_challenge(self):
        cursor = self.db_conn.cursor()
        cursor.execute(self.db_queries['GET_NEW_CHALLENGE'])
        challenge = cursor.fetchall()
        if challenge == []:
            messageLogger.critical("No new challenges left in the database, can't send any challenge today")
        else:
            today_challenge = challenge[0]
            self.challenge_dict = {
                "id": today_challenge[0],
                "description": today_challenge[1],
                "modification": today_challenge[2],
                "calories": today_challenge[3],
                "place": today_challenge[4],
                "url": today_challenge[5],
                "is_used": today_challenge[6],
                "used_date": today_challenge[7]
            }
            
        cursor.execute(self.db_queries['MARK_CHALLENGE_DONE']%(self.challenge_dict['id']))
        self.db_conn.commit()
        self.db_conn.close()

    def send_challenge(self):
        self.load_challenge()
        
        try:
            result = self.client.chat_postMessage(
                channel= self.channel_id_mapping['bot_testing'], 
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"""
Good Morning <!channel>
Here is today's Tenacity challenge:

*Challenge* :dart:
{self.challenge_dict['description']}
Here is a quick explainer video: {self.challenge_dict['url']}

*Modification* :hammer_and_wrench:
{self.challenge_dict['modification']}

*Estimated Calories Burnt* :fire:
{self.challenge_dict['calories']}

*What is the most optimal place to do today's challenge* :house:
{self.challenge_dict['place']}

Reply to this message with :white_check_mark: once you are done with the challenge.
"""
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "value": "challenge_completed",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Completed :thumbsup:",
                                    "emoji": True
                                }
                            },
                            {
                                "type": "button",
                                "value": "challenge_not_completed",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Not Completed :thumbsdown:",
                                    "emoji": True,
                                }
                            }
                        ]
                    }
                ]
            )
            messageLogger.info("Morning channel posted")
        except SlackApiError as e:
            messageLogger.error(f"Error posting message: {e}")

challenge = MorningChallenge()
challenge.send_challenge()