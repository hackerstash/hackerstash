import random
from hackerstash.lib.redis import redis


class Tokens:
    @classmethod
    def verify(cls, email, code):
        token = redis.get(f'token:{email}')
        return token.decode('utf-8') == str(code) if token else False

    @classmethod
    def generate(cls, email):
        code = random.randint(100000, 999999)
        redis.set(f'token:{email}', code)
        return code

    @classmethod
    def delete(cls, email):
        redis.delete(f'token:{email}')
