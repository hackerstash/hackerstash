from flask import url_for
from sqlalchemy import or_
from hackerstash.models.comment import Comment
from hackerstash.models.post import Post
from hackerstash.models.project import Project
from hackerstash.models.user import User


def universal_search(query):
    return {
        'comments': get_comments(query),
        'posts': get_posts(query),
        'projects': get_projects(query),
        'users': get_users(query)
    }


def get_comments(query):
    comments = Comment.query.filter(or_(
        Comment.body.ilike(f'%{query}%')
    ))
    return list(map(get_comment_payload, comments))


def get_posts(query):
    posts = Post.query.filter(or_(
        Post.title.ilike(f'%{query}%'),
        Post.body.ilike(f'%{query}%')
    )).all()
    return list(map(get_post_payload, posts))


def get_projects(query):
    projects = Project.query.filter(or_(
        Project.name.ilike(f'%{query}%'),
        Project.description.ilike(f'%{query}%')
    )).all()
    return list(map(get_project_payload, projects))


def get_users(query):
    users = User.query.filter(or_(
        User.username.ilike(f'%{query}%'),
        User.first_name.ilike(f'%{query}%'),
        User.last_name.ilike(f'%{query}%'),
        User.bio.ilike(f'%{query}%')
    )).all()
    return list(map(get_user_payload, users))


def get_comment_payload(comment):
    return {
        'body': comment.body,
        'url': url_for('posts.show', post_id=comment.post.url_slug) + '#' + str(comment.id)
    }


def get_post_payload(post):
    return {
        'title': post.title,
        'body': post.body,
        'url': url_for('posts.show', post_id=post.url_slug)
    }


def get_project_payload(project):
    return {
        'name': project.name,
        'description': project.description,
        'url': url_for('projects.show', project_id=project.id)
    }


def get_user_payload(user):
    return {
        'name': f'{user.first_name} {user.last_name}',
        'username': user.username,
        'bio': user.bio,
        'url': url_for('users.show', user_id=user.id)
    }
