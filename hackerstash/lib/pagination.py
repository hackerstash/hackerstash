import math
from flask import request


def paginate(iterator, limit=25):
    page = int(request.args.get('page', 1))
    total_pages = math.ceil(len(iterator) / limit)

    pagination = {
        'pages': total_pages,
        'current': page
    }

    start = (page - 1) * limit
    end = start + limit

    return list(iterator)[start:end], pagination
