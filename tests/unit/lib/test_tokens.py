from unittest.mock import patch
from hackerstash.lib.tokens import Tokens


class TestTokens:
    email = 'foo@bar.com'

    @patch('redis.Redis.get')
    def test_verify_when_token_is_incorrect(self, redis):
        redis.return_value = b'123456'
        assert Tokens.verify(self.email, '54321') is False
        assert redis.called_with(f'token:{self.email}')

    @patch('redis.Redis.get')
    def test_verify_when_token_is_correct(self, redis):
        redis.return_value = b'123456'
        assert Tokens.verify(self.email, '123456') is True
        assert redis.called_with(f'token:{self.email}')

    @patch('random.randint')
    @patch('redis.Redis.set')
    def test_generate(self, redis, randint):
        redis.return_value = None
        randint.return_value = 123456
        assert Tokens.generate(self.email) == 123456
        assert redis.called_with(f'token:{self.email}', 123456)

    @patch('redis.Redis.delete')
    def test_delete(self, redis):
        redis.return_value = None
        assert Tokens.delete(self.email) is None
        assert redis.called_with(f'token:{self.email}')
