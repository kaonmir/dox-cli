import click


@click.group()
def gitlab():
    """Check the current directory for documentation errors"""
    pass


from .create_group import create_group
from .list_project import list_project

gitlab.add_command(list_project)
gitlab.add_command(create_group)
