from typing import Union
from hackerstash.lib.webhooks.types.delete_user import DeleteUser
from hackerstash.lib.webhooks.types.end_contest import EndContest

webhook_factory_response = Union[
    DeleteUser,
    EndContest
]


def webhook_factory(event_type: str, payload: dict) -> webhook_factory_response:
    """
    Process a new webhook event
    :param event_type: str
    :param payload: dict
    :return: webhook_factory_response
    """
    if event_type == 'delete_user':
        return DeleteUser(payload)
    if event_type == 'end_contest':
        return EndContest(payload)

    raise Exception(f'{event_type} is not a valid webhook type')
