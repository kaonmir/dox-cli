import click

# @click.command()
# @click.option("--count", default=1, help="Number of greetings.")
# @click.option("--name", prompt="Your name", help="The person to greet.")
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo(f"Hello {name}!")

from .check import check
from .gitlab import gitlab


@click.group()
def cli():
    pass


cli.add_command(check)
cli.add_command(gitlab)
