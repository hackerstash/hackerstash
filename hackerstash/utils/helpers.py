def find_in_list(iterable, predicate=None):
    """
    Returns the first truthy value in the iterable
    Example:
    first_in_list([{'foo': 'bar'}], predicate=lambda x: x == 'bar')
    """
    return next(filter(predicate, iterable), None)
