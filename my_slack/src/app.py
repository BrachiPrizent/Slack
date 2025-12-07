import getopt
import logging
import os
import sys
from dotenv import load_dotenv
from slack_sdk import WebClient
from connecting_to_slack import get_list_of_channels, get_list_of_users, send_slack_message

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

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='app.log',
        filemode='a'
    )
    main(sys.argv[1:])
