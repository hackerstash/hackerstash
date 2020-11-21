import sys
import json
import traceback


class Logging:
    def __init__(self, module: str = None):
        """
        Initialise an instance of the logging class
        :param module: str
        """
        self.module = module

    def _log(self, msg: str, payload: dict, level: str):
        """
        Log the message to STDOUT
        :param msg: str
        :param payload: dict
        :param level: str
        :return: None
        """
        payload = payload or {}
        log = {
            'message': msg,
            'level': level,
            'module': self.module,
            **payload
        }
        print(json.dumps(log))

    def debug(self, msg: str, payload: dict = None):
        """
        Log a debug message
        :param msg: str
        :param payload: dict
        :return: None
        """
        self._log(msg, payload, 'DEBUG')

    def info(self, msg: str, payload: dict = None):
        """
        Log an info message
        :param msg: str
        :param payload: dict
        :return: None
        """
        self._log(msg, payload, 'INFO')

    def warn(self, msg: str, payload: dict = None):
        """
        Log an warn message
        :param msg: str
        :param payload: dict
        :return: None
        """
        self._log(msg, payload, 'WARN')

    def error(self, msg: str, error: Exception):
        """
        Log an error message
        :param msg: str
        :param error: Exception
        :return: None
        """
        payload = {
            'error': repr(error),
            'stack': get_traceback(error)
        }
        self._log(msg, payload, 'ERROR')


def get_traceback(error: Exception) -> str:
    """
    Extract the traceback in a string format so that
    it can be logged to Cloudwatch safely
    :param error: Exception
    :return: str
    """
    exc_traceback = sys.exc_info()[2]
    stack = ''.join(traceback.format_tb(exc_traceback))
    return stack + '    ' + str(error)

