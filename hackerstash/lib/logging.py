import sys
import json
import traceback


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


def get_traceback(error):
    exc_traceback = sys.exc_info()[2]
    stack = ''.join(traceback.format_tb(exc_traceback))
    return stack + '    ' + str(error)

