import arrow
from enum import Enum


class GoalStates(Enum):
    SET = 'SET'
    EDIT = 'EDIT'
    REFLECT = 'REFLECT'
    REVIEW = 'REVIEW'
    NONE = 'NONE'


class Goals:
    def __init__(self, project):
        """
        Initialise a new instance of the goals class
        :param project: Project
        """
        self.now = arrow.utcnow()
        self.goals = project.active_goals

    def status(self):
        """
        Returns the enum for the current state of the goals. If nothing
        matches then they failed to participate and we should hide the
        goals stuff from them
        :return: GoalStates
        """
        if self.is_set:
            return GoalStates.SET
        if self.is_edit:
            return GoalStates.EDIT
        if self.is_reflect:
            return GoalStates.REFLECT
        if self.is_review:
            return GoalStates.REVIEW

        return GoalStates.NONE

    @property
    def is_set(self) -> bool:
        """
        From Monday morning and Tuesday night, only if they have not
        set their goals
        :return: bool
        """
        start = arrow.utcnow().floor('week')
        end = start.shift(days=1).ceil('day')
        return not self.goals and start < self.now < end

    @property
    def is_edit(self) -> bool:
        """
        From Monday morning and Tuesday night, only if they HAVE set
        their goals
        :return: bool
        """
        start = arrow.utcnow().floor('week')
        end = start.shift(days=1).ceil('day')
        return self.goals and start < self.now < end

    @property
    def is_reflect(self) -> bool:
        """
        From Wednesday morning to Saturday night, only if they have set
        their goals
        :return: bool
        """
        start = arrow.utcnow().floor('week').shift(days=2)
        end = start.shift(days=3).ceil('day')
        return self.goals and start < self.now < end

    @property
    def is_review(self) -> bool:
        """
        From Sunday morning to Sunday night, only if they have reflected
        on their goals
        :return: bool
        """
        start = arrow.utcnow().floor('week').shift(days=6)
        end = start.ceil('day')
        reflected = self.goals and all([goal.completed for goal in self.goals])
        return reflected and start < self.now < end
