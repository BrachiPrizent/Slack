import getopt
import logging
import sys

from src.connecting_to_slack import connectToSlack

logger = logging.getLogger(__name__)

def get_message(argv):
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
            connectToSlack(message)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='app.log',
        filemode='a'
    )
    get_message(sys.argv[1:])
