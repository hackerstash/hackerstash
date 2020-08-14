from hackerstash.lib.logging import logging
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
    projects = Project.query.filter_by(published=True)
    args = get_args(args)

    if len(args) == 0:
        return list(projects)

    logging.info('Filtering projects %s', args)

    projects = sort_projects(projects, args.get('sorting'))
    projects = filter_projects(projects, args)
    return projects


def get_args(raw_args) -> dict:
    args = {}
    for key, value in raw_args.to_dict().items():
        if value and value != 'Please select':
            if key in ['platforms_and_devices', 'business_models', 'fundings']:
                args[key] = raw_args.getlist(key)
            else:
                args[key] = value
    return args


def filter_projects(projects, args):
    args.pop('sorting', None)
    out = []

    for project in projects:
        if all(filter_by_arg(project, key, value) for key, value in args.items()):
            out.append(project)

    return out


def filter_by_arg(project, key: str, value: str) -> bool:
    if not value:
        return True
    if key == 'member_count':
        return filter_by_team_size(len(project.members), value)
    if key == 'time_commitment':
        return filter_by_time_commitment(project.time_commitment, value)
    if key == 'country':
        return filter_by_country(project.location, value)
    if key == 'platforms_and_devices':
        return filter_by_platforms_and_devices(project.platforms_and_devices, value)
    if key == 'business_models':
        return filter_by_business_models(project.business_models, value)
    if key == 'fundings':
        return filter_by_fundings(project.fundings, value)
    return True


def filter_by_team_size(member_count: int, value: str) -> bool:
    return member_count == 1 if value == 'SOLO' else member_count > 1


def filter_by_time_commitment(time_commitment: str, value: str) -> bool:
    return time_commitment.lower() == value


def filter_by_country(country: str, value: str) -> bool:
    return country.find(value) != -1


def filter_by_platforms_and_devices(platfroms_and_devices: list, value: str) -> bool:
    return all(x in platfroms_and_devices for x in value)


def filter_by_business_models(business_models: list, value: str) -> bool:
    return all(x in business_models for x in value)


def filter_by_fundings(fundings: list, value: str) -> bool:
    return all(x in fundings for x in value)


def sort_projects(projects, sorting: str = 'alphabetical_desc'):
    # It would be nice to do this at the database level
    # but some stuff like the vote_score is calculated
    # after load so it's not currently possible
    if sorting == 'alphabetical_desc':
        return sorted(projects, key=lambda x: x.name[0], reverse=True)
    if sorting == 'alphabetical_asc':
        return sorted(projects, key=lambda x: x.name[0], reverse=False)
    if sorting == 'rank_desc':
        return sorted(projects, key=lambda x: x.vote_score, reverse=True)
    if sorting == 'rank_asc':
        return sorted(projects, key=lambda x: x.vote_score, reverse=False)
    if sorting == 'created_at_desc':
        return sorted(projects, key=lambda x: x.created_at, reverse=True)
    if sorting == 'created_at_asc':
        return sorted(projects, key=lambda x: x.created_at, reverse=False)
    if sorting == 'team_size_desc':
        return sorted(projects, key=lambda x: len(x.members), reverse=True)
    if sorting == 'team_size_asc':
        return sorted(projects, key=lambda x: len(x.members), reverse=False)
    return projects
