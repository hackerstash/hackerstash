from flask import request
from hackerstash.models.comment import Comment

# This file is wank, I'd really love to do this all at the database level
# with unions or some shit but I'm too dumb to figure it out.
#
# The great hero who overcomes this mess may sign here:
#
# ________________________________


class Feed:
    def __init__(self, project):
        self.project = project
        self.limit = 10
        self.has_next = False
        self.page = request.args.get('page', 1, type=int)
        self.show = request.args.getlist('show') or ['posts', 'polls', 'comments']

    @property
    def comments(self):
        if 'comments' not in self.show:
            return []
        ids = [member.user_id for member in self.project.members]
        return Comment.query.filter(Comment.user_id.in_(ids)).all()

    @property
    def posts(self):
        if 'posts' not in self.show and 'polls' not in self.show:
            return []
        posts = self.project.posts
        # Remove posts if we just want polls
        if 'posts' not in self.show:
            posts = list(filter(lambda x: x.poll, posts))
        # Remove polls if we just want posts
        if 'polls' not in self.show:
            posts = list(filter(lambda x: not x.poll, posts))
        return posts

    @property
    def items(self) -> list:
        out = [*self.comments, *self.posts]
        return self.paginate(out)

    @property
    def next_page(self):
        return self.page + 1 if self.has_next else self.page

    def paginate(self, out):
        # Sort by created date
        results = sorted(out, key=lambda x: x.created_at, reverse=True)
        self.has_next = len(out) >= self.page * self.limit

        return results[:self.limit * self.page]
