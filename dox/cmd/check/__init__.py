import click


@click.group()
def check():
    """Check the current directory for documentation errors"""
    pass


from .network import network
from .hardware import hardware
from .list_project import list_project


check.add_command(network)
check.add_command(hardware)
check.add_command(list_project)
