import random
from hackerstash.lib.redis import redis


class Tokens:
    @classmethod
    def verify(cls, email: str, code: str) -> bool:
        """
        Verify that a stored token both exists, and is valid
        :param email: str
        :param code: str
        :return: bool
        """
        token = redis.get(f'token:{email}')
        return token.decode('utf-8') == str(code) if token else False

    @classmethod
    def generate(cls, email: str) -> int:
        """
        Generate and store a new token
        :param email: str
        :return: int
        """
        code = random.randint(100000, 999999)
        redis.set(f'token:{email}', code)
        return code

    @classmethod
    def delete(cls, email: str) -> None:
        """
        Delete a stored token if it exists
        :param email: str
        :return: None
        """
        redis.delete(f'token:{email}')
