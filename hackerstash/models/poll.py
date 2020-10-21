from uuid import uuid4
from flask import g
from sqlalchemy.types import JSON
from sqlalchemy.orm.attributes import flag_modified
from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.utils.helpers import find_index, find_in_list

log = Logging(module='Models::Poll')


class Poll(db.Model):
    __tablename__ = 'polls'

    id = db.Column(db.Integer, primary_key=True)

    question = db.Column(db.String, nullable=False)
    choices = db.Column(JSON(none_as_null=True))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Poll {self.question}>'

    def __init__(self, question: str, choices: list, post):
        self.question = question
        self.post = post
        self.choices = [{'id': str(uuid4()), 'name': c, 'user_ids': []} for c in choices]

    @property
    def all_answered_user_ids(self):
        return sum([c['user_ids'] for c in self.choices], [])

    @property
    def has_answered(self):
        return g.user.id in self.all_answered_user_ids

    def answer(self, choice: str):
        if not self.has_answered:
            position = find_index(self.choices, 'id', choice)
            if position != -1:
                self.choices[position]['user_ids'].append(g.user.id)
                # SQLAlchemy needs to be told we modified the list
                flag_modified(self, 'choices')
                db.session.commit()
            else:
                log.warn('Position was out of range', {'choices': self.choices, 'choice': choice})

    def get_percentage_for_choice(self, choice_id):
        # Flatten all of the user_ids
        total = len(self.all_answered_user_ids)
        if total == 0:
            return 0
        choice = find_in_list(self.choices, lambda x: x['id'] == choice_id)
        return int((len(choice['user_ids']) / total) * 100)

    def has_answered_choice(self, choice_id: str):
        if 'user' not in g:
            return False
        choice = find_in_list(self.choices, lambda x: x['id'] == choice_id)
        return g.user.id in choice['user_ids']
