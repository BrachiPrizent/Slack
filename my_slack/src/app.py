import getopt
import logging
import os
import requests
import sys
from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()
logger = logging.getLogger(__name__)

def main(argv):
    message = ' '
    try: 
        opts, args = getopt.getopt(argv, "hm:", ["message="])

    except getopt.GetoptError:
        logger.info('slack.py -m <message>')
        sys.exit(2)

    if len(opts) == 0:
        message = 'HELLO, WORLD!'
    for opt, arg in opts:
        if opt == '-h':
            logger.info('slack.py -m <message>')
            sys.exit()
        elif opt in ("-m", "--message"):
            message = arg

    send_slack_message(message)
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    client = WebClient(token=slack_token)
    get_list_of_channels(client)
    get_list_of_users(client)

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
            logger.info("- Name: %s, ID: %s, Email: %s", {user['name']}, {user['id']}, {user['email']})

    except Exception as e:
        logger.error("Error fetching users: %s", {e})

def get_list_of_channels(client):
    try:
        response = client.conversations_list(types="public_channel")
        channels = response["channels"]
        channel_list = []
        for channel in channels:
            channel_list.append({
                "name": channel["name"],
                "id": channel["id"]
            })
        logger.info("\nConnected Channel List:")
        for channel in channel_list:
            logger.info("- Name: %s, ID: %s", {channel['name']}, {channel['id']})

    except Exception as e:
        logger.error("Error fetching channels: %s", {e})

def send_slack_message(message):
    payload = {"text": message}
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
    response = requests.post(SLACK_WEBHOOK_URL, json = payload, verify=False)
    logger.info("Status: %s", response.status_code)
    logger.info("Response: %s", response.text)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='app.log',
        filemode='a'
    )
    main(sys.argv[1:])
