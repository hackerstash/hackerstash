import datetime
from hackerstash.models.challenge import Challenge


class Base:
    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the Challenge base class
        :param payload: dict
        """
        self.payload = payload

    @property
    def month(self) -> int:
        """
        Get the correct month to use for this challenge
        :return: int
        """
        now = datetime.datetime.now()
        return now.month

    @property
    def year(self) -> int:
        """
        Get the correct year to use for this challenge
        :return: int
        """
        now = datetime.datetime.now()
        return now.year

    def has_completed(self, project, key: str) -> bool:
        """
        Return whether or not this challenge has been completed
        :param project: Project
        :param key: str
        :return: bool
        """
        return Challenge.has_completed_key(project, key)
