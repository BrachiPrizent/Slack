import logging
import os
import requests
from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()
logger = logging.getLogger(__name__)

def connectToSlack(message):
    send_slack_message(message)
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    client = WebClient(token=slack_token)
    get_list_of_channels(client)
    get_list_of_users(client)


def send_slack_message(message):
    payload = {"text": message}
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
    response = requests.post(SLACK_WEBHOOK_URL, json = payload, verify=False)
    logger.info("Status: %s", response.status_code)
    logger.info("Response: %s", response.text)

def get_list_of_channels(client):
    try:
        response = client.conversations_list(types="public_channel")
        channels = response["channels"]
        channels_list = []
        for channel in channels:
            channels_list.append({
                "name": channel["name"],
                "id": channel["id"]
            })
        logger.info("\nConnected Channel List:")
        for channel in channels_list:
            logger.info("- Name: %s, ID: %s", channel['name'], channel['id'])

    except Exception as e:
        logger.error("Error fetching channels: %s", {e})

def get_list_of_users(client):
    try:
        response = client.users_list()
        members = response["members"]
        user_list = []
        for member in members:
            if not member['is_bot'] and not member['deleted']:
                user_list.append({
                    "name": member.get("real_name", member.get("name")),
                    "id": member["id"],
                    "email": member["profile"].get("email")
                })
        logger.info("Connected User List:")
        for user in user_list:
            logger.info("- Name: %s, ID: %s, Email: %s", user['name'], user['id'], user['email'])

    except Exception as e:
        logger.error("Error fetching users: %s", {e})
