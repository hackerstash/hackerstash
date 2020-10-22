import bleach


def find_in_list(iterable, predicate=None):
    """
    Returns the first truthy value in the iterable
    Example:
    find_in_list([{'foo': 'bar'}], predicate=lambda x: x == 'bar')
    """
    return next(filter(predicate, iterable), None)


def find_index(iterable, key, value):
    """
    Returns the index of the dict in the list if it exists
    Example:
    find_index([{'key': 'foo'}], 'key', 'foo')
    """
    for i, item in enumerate(iterable):
        if item[key] == value:
            return i
    return -1


def html_to_plain_text(value: str, limit: int = None) -> str:
    text = bleach.clean(value or '', tags=[], strip=True)
    if limit and len(text) > limit:
        text = text[:limit - 3] + '...'
    return text


def get_html_text_length(html: str) -> int:
    text = html_to_plain_text(html).strip()
    return len(text)
