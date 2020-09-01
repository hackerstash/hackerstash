import os
import logging
from gunicorn import glogging


class GunicornLogger(glogging.Logger):
    def setup(selfself, cfg):
        super().setup(cfg)
        logger = logging.getLogger('gunicorn.access')
        logger.addFilter(HealthCheckFilter())


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return '/__ping' not in record.getMessage()


bind = '0.0.0.0:5000'
workers = 2
threads = 4
reload = os.environ.get('DEBUG', False)
accesslog = '-'
access_log_format = '{"address":"%(h)s", "method":"%(m)s", "url":"%(U)s", "status":%(s)s, "duration":%(T)s, "pid":"%(p)s"}'
logger_class = GunicornLogger
