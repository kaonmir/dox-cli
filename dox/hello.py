import click


@click.command()
@click.argument(
    "name",
    default="World",
)
def hello(name):
    """Say hello"""
    print(f"Hello {name}")
