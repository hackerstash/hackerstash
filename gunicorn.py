import os

bind = '0.0.0.0:5000'
workers = 2
threads = 4
reload = os.environ.get('DEBUG', False)
accesslog = '-'
access_log_format = '{"address":"%(h)s", "date":"%(t)s", "method":"%(m)s", "url":"%(U)s", "status":"%(s)s", "duration":"%(T)s", "pid":"%(p)s"}'
