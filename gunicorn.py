import os
import logging
from gunicorn import glogging


class GunicornLogger(glogging.Logger):
    def setup(self, cfg):
        super().setup(cfg)
        logger = logging.getLogger('gunicorn.access')
        logger.addFilter(AccessLogExcludes())


class AccessLogExcludes(logging.Filter):
    # These are noise in the logs we don't need
    exclude = ['/__ping', '/static/', '/notifications/count']

    def filter(self, record):
        url = record.args.get('U', '')
        return all(not url.startswith(x) for x in self.exclude)


bind = '0.0.0.0:5000'
workers = 2
threads = 4
reload = os.environ.get('DEBUG', False)
accesslog = '-'
access_log_format = '{"address":"%(h)s", "method":"%(m)s", "url":"%(U)s", "status":%(s)s, "duration":%(L)s, "pid":"%(p)s", "user-agent": "%(a)s", "referer": "%(f)s", "size": "%(B)s"}'
logger_class = GunicornLogger
