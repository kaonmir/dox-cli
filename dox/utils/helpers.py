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
        raise click.ClickException(f"File {file} does not exist")

    file_type = file.split(".")[-1]
    if file_type == "yaml" or file_type == "yml":
        try:
            with open(file) as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            click.ClickException(f"File {file} is not a valid yaml file")
    elif file_type == "json":
        try:
            with open(file) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            click.ClickException(f"File {file} is not a valid json file")
    else:
        click.ClickException(f"File {file} is not a valid yaml or json file")
