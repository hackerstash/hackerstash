import logging

logging_format = '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "origin": "%(filename)s:%(lineno)d", "message": "%(message)s"}'

logging.basicConfig(format=logging_format, level=logging.INFO)
