import click


@click.group()
def check():
    """Check commands"""
    pass


from .network import network
from .hardware import hardware


check.add_command(network)
check.add_command(hardware)
