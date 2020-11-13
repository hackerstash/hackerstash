from hackerstash.db import db
from hackerstash.lib.leaderboard import Leaderboard
from hackerstash.models.post import Post
from hackerstash.models.project import Project


class Given:
    @classmethod
    def a_project_exist(cls):
        p = Project(name=f'project_1', published=True)
        db.session.add(p)
        db.session.commit()
        return p

    @classmethod
    def a_bunch_of_projects_exist(cls, count=5):
        projects = []
        for i in range(count):
            p = Project(name=f'project_{i}', published=True)
            projects.append(p)
            db.session.add(p)
        db.session.commit()
        return projects

    @classmethod
    def a_bunch_of_projects_exist_on_the_leaderboard(cls, count=5):
        projects = cls.a_bunch_of_projects_exist(count)
        for index, project in enumerate(projects):
            Leaderboard(project).update(index * 10)

    @classmethod
    def a_bunch_of_posts_exist(cls, project, count=5):
        posts = []
        for i in range(count):
            p = Post(title=f'title={i}', body='sdfsdf', url_slug=f'title_{i}', project=project)
            db.session.add(p)
        db.session.commit()
        return posts
