import os
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

import sys
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from modules.message import Message
from logger.logger import messageLogger
from slack_sdk.errors import SlackApiError
from datetime import date
import calendar

class ReminderNudge(Message):
    def __init__(self):
        super().__init__()        

    def send_nudge(self):
        curr_date = date.today()
        day = calendar.day_name[curr_date.weekday()]
        try:
            result = self.client.chat_postMessage(
                channel= self.channel_id_mapping['bot_testing'], 
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"""
Hello Astraaaaaa!

Happy {day} :smiley:

Make sure to get your challenge in for the day.  Don't forget to react once you're done! :white_check_mark:"
"""
                        }
                    }
                ]
            )
            messageLogger.info("Reminder nudge posted")
        except SlackApiError as e:
            messageLogger.error(f"Error posting message: {e}")

challenge = ReminderNudge()
challenge.send_nudge()