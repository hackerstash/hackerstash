import os

bind = '0.0.0.0:5000'
workers = 2
threads = 4
reload = os.environ.get('DEBUG', False)
accesslog = '-'
access_log_format = '%(h)s %(l)s %(t)s \'%(r)s\' %(s)s'
