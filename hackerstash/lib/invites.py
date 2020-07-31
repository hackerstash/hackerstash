import jwt


def generate_invite_link(email):
    token = jwt.encode({'email': email}, 'secret', algorithm='HS256')  # TODO use config for secret
    return f'http://localhost:5000/projects/invites/{token}'
