import click


@click.group()
def gitlab():
    """Check the current directory for documentation errors"""
    pass


from .list_project import list_project

gitlab.add_command(list_project)
