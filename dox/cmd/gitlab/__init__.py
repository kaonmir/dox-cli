import click


@click.group()
def gitlab():
    """Gitlab commands"""
    pass


from .create_group import create_group
from .list_project import list_project

gitlab.add_command(list_project)
gitlab.add_command(create_group)
