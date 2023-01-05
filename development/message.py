import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import date
import calendar

import logging
from logger.logger import messageLogger 

class Message:
    def __init__(self):
        try:
            with open("./config/credentials.json", 'r') as file:
                    self.credentials = json.load(file)
        except FileNotFoundError as e:
            raise Exception(e)

        self.channel_id_mapping = {
            "bot_testing": "C03D2NCT06R"
        }

        self.client = WebClient(token=self.credentials['bot_oauth_token'])

    def send_challenge(self, challenge, modification, calories, place, url):
        try:
            result = self.client.chat_postMessage(
                channel= self.channel_id_mapping['bot_testing'], 
                blocks= [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Good Morning <!channel>\nHere is today's Tenacity challenge:\n"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Challenge* :dart:\n{challenge}\nHere is a quick explainer video: {url}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Modification* :hammer_and_wrench:\n{modification}\n"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Estimated Calories Burnt* :fire:\n{calories}\n"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*What is the most optimal place to do today's challenge* :house:\n{place}\n"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Are you ready to accept the challenge ?"
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "value": "challenge_accepted",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Yes :thumbsup:",
                                    "emoji": True
                                }
                            },
                            {
                                "type": "button",
                                "value": "challenge_rejected",
                                "text": {
                                    "type": "plain_text",
                                    "text": "No :thumbsdown:",
                                    "emoji": True,
                                }
                            }
                        ]
                    }
                ]
            )
            self.logger.info(result)

        except SlackApiError as e:
            self.logger.error(f"Error posting message: {e}")
        
    def send_dm(self):
        self.client.chat_postMessage(channel="U03D51Z31T5", text="hello")

    def load_challenge(self):
        self.send_challenge(
            challenge="50 Mountain Climbers Each Side, that is, 100 reps overall!",
            modification="No modification required",
            calories="67.2",
            place="Home Sweet Home",
            url="https://www.youtube.com/watch?v=wJiUnvP_pcU"
        )

    def send_nudge(self):
        try:
            curr_date = date.today()
            day = calendar.day_name[curr_date.weekday()]
            result = self.client.chat_postMessage(
                channel= self.channel_id_mapping['bot_testing'], 
                blocks= [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Hello Astraaaaaa!\nHappy {day} :smiley:\nMake sure to get your challenge in for the day. Don't forget to react once you're done! :white_check_mark:"
                        }
                    }
                ]
            )
            self.logger.info(result)

        except SlackApiError as e:
            self.logger.error(f"Error posting message: {e}")

    def test(self):
        x = self.client.users_list()
        file = open("users.json", 'a')
        for p in x.data['members']:
            json.dump(p, file, indent=4)

    def send_weekly_update(self):
        try:
            result = self.client.chat_postMessage(
                channel= self.channel_id_mapping['bot_testing'], 
                blocks= [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f""":rotating_light: Tenacity Weekly Update! :rotating_light:
                            Hello <!channel> :wave:
                            Here are the stats from last week. :point_down:"""
                        }
                    }
                ]
            )
            self.logger.info(result)

        except SlackApiError as e:
            self.logger.error(f"Error posting message: {e}")
