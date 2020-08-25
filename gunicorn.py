import os

bind = '0.0.0.0:5000'
workers = 2
threads = 4
reload = os.environ.get('DEBUG', False)
accesslog = '-'
access_log_format = '{"address":"%(h)s", "method":"%(m)s", "url":"%(U)s", "status":%(s)s, "duration":%(M)s, "pid":"%(p)s"}'
