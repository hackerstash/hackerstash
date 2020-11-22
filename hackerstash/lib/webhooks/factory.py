from typing import Union
from hackerstash.lib.webhooks.types.delete_user import DeleteUser
from hackerstash.lib.webhooks.types.end_contest import EndContest
from hackerstash.lib.webhooks.types.prepare_feedback import PrepareFeedback
from hackerstash.lib.webhooks.types.project_vote_reminder import ProjectVoteReminder

webhook_factory_response = Union[
    DeleteUser,
    EndContest,
    PrepareFeedback,
    ProjectVoteReminder
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
    if event_type == 'prepare_feedback':
        return PrepareFeedback(payload)
    if event_type == 'project_vote_reminder':
        return ProjectVoteReminder(payload)

    raise Exception(f'{event_type} is not a valid webhook type')
