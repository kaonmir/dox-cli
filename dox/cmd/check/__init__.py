import click


@click.group()
def check():
    """Check the current directory for documentation errors"""
    pass


from .smtp import smtp
from .hardware import hardware
from .list_project import list_project


check.add_command(smtp)
check.add_command(hardware)
check.add_command(list_project)
