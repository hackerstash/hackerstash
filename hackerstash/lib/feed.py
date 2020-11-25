from typing import Union
from flask import request
from hackerstash.models.comment import Comment
from hackerstash.models.post import Post

FeedList = list[Union[Post, Comment]]


class Feed:
    def __init__(self, project):
        """
        Initialise a new instance of the feed class
        :param project: Project
        """
        self.project = project
        self.limit = 10
        self.has_next = False
        self.page = request.args.get('page', 1, type=int)
        self.show = request.args.getlist('show') or ['posts', 'polls', 'comments']

    @property
    def comments(self) -> [Comment]:
        """
        Get a list of all the comments made by members of
        this project. If comments are not selected it returns
        an empty array
        :return: [Comment]
        """
        if 'comments' not in self.show:
            return []
        ids = [member.user_id for member in self.project.members]
        return Comment.query.filter(Comment.user_id.in_(ids)).all()

    @property
    def posts(self) -> [Post]:
        """
        Get a list of posts made by users of this project. If
        either the posts or polls are not selected it returns an
        empty array
        :return: [Post]
        """
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
    def items(self) -> FeedList:
        """
        Return a paginated list of the results. They can be a mixture
        of Posts or Comments depending on the selection
        :return: FeedList
        """
        out = [*self.comments, *self.posts]
        return self.paginate(out)

    @property
    def next_page(self) -> int:
        """
        Returns the next page for pagination. If there are no more
        results it returns the current page
        :return: int
        """
        return self.page + 1 if self.has_next else self.page

    def paginate(self, out: FeedList) -> FeedList:
        """
        Paginate the results based on the limit/offset
        :param out: FeedList
        :return: FeedList
        """
        # Sort by created date
        results = sorted(out, key=lambda x: x.created_at, reverse=True)
        self.has_next = len(out) >= self.page * self.limit

        return results[:self.limit * self.page]
