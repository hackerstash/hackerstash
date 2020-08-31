import sys
import logging
import traceback
import requests
from hackerstash.config import config


def log_stacktrace(error):
    # This is required as cloudwatch will print each line in the
    # native exception as it's own entry which is impossible to
    # debug. Instead we format the exception and pass it into the
    # logger so dumped as JSON
    exc_type, exc_value, exc_traceback = sys.exc_info()
    stack = ''.join(traceback.format_tb(exc_traceback)).strip().replace('"', '\\"').replace('\n', '')
    logging.error(stack + '    ' + str(error))


def publish_slack_message(error):
    if config['app_environment'] == 'live':
        try:
            url = f'https://hooks.slack.com/services/{config["error_webhook"]}'
            payload = {
                'username': '500 Error',
                'icon_emoji': ':octagonal_sign:',
                'attachments': [{'color': 'danger', 'text': str(error)}]
            }
            headers = {
                'Content-Type': 'application/json'
            }
            requests.request('POST', url, headers=headers, json=payload)
        finally:
            pass


logging_format = '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "origin": "%(filename)s:%(lineno)d", "message": "%(message)s"}'

logging.basicConfig(format=logging_format, level=logging.INFO)
logging.stack = log_stacktrace
