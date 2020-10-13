import sys
import json
import traceback
import requests
from hackerstash.config import config


class Logging:
    def __init__(self, module: str = None):
        self.module = module

    def _log(self, msg, payload, level):
        payload = payload or {}
        log = {
            'message': msg,
            'level': level,
            'module': self.module,
            **payload
        }
        print(json.dumps(log))

    def debug(self, msg, payload=None):
        self._log(msg, payload, 'DEBUG')

    def info(self, msg, payload=None):
        self._log(msg, payload, 'INFO')

    def warn(self, msg, payload=None):
        self._log(msg, payload, 'WARN')

    def error(self, msg, error):
        payload = {
            'error': repr(error),
            'stack': get_traceback(error)
        }
        self._log(msg, payload, 'ERROR')
        publish_slack_message(error)


def get_traceback(error):
    exc_traceback = sys.exc_info()[2]
    stack = ''.join(traceback.format_tb(exc_traceback))
    return stack + '    ' + str(error)


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

