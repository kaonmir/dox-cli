import os
import click
import yaml
import json


def toTB(x):
    return x / (1024**4)


def toGB(x):
    return x / (1024**3)


def open_structured_file(file):
    file = os.path.abspath(file)
    if not os.path.exists(file):
        click.echo(f"File {file} does not exist")
        exit(1)

    file_type = file.split(".")[-1]
    if file_type == "yaml" or file_type == "yml":
        try:
            with open(file) as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            click.echo(f"File {file} is not a valid yaml file")
            click.echo(e)
            exit(1)
    elif file_type == "json":
        try:
            with open(file) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            click.echo(f"File {file} is not a valid json file")
            click.echo(e)
            exit(1)
    else:
        click.echo(f"File {file} is not supported")
        exit(1)
