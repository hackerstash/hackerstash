import redis as redis_client
from hackerstash.config import config

redis = redis_client.Redis(host=config['redis_host'], port=config['redis_port'], db=0)
