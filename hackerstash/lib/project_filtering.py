from hackerstash.models.project import Project

filter_args = [
    'team_size',
    'time_commitment',
    'country',
    'platforms_and_devices',
    'business_models',
    'fundings'
]


def project_filtering(args):
    base = Project.query.filter_by(published=True)
    args = get_args(args)

    if len(args) == 0:
        return base

    # TODO
    print(args)
    return base


def get_args(raw_args):
    args = {}
    for key, value in raw_args.to_dict().items():
        if value and value != 'Please select':
            args[key] = value
    return args
