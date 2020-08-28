import redis as redis_client
from hackerstash.config import config

redis = redis_client.Redis(host=config['redis_host'], port=6379, db=0)
