import click
import gitlab
import os
import requests


def load_gitlab(GITLAB_URL, GITLAB_PRIVATE_TOKEN):
    if not GITLAB_URL:
        click.echo("GITLAB_URL not set")
        exit(1)
    if not GITLAB_PRIVATE_TOKEN:
        click.echo("GITLAB_PRIVATE_TOKEN not set")
        exit(1)

    try:
        timeout_duration = 2
        requests.get(GITLAB_URL, timeout=timeout_duration)
    except requests.exceptions.ConnectionError:
        raise Exception(f"Unable to connect to {GITLAB_URL}")

    gl = gitlab.Gitlab(GITLAB_URL, GITLAB_PRIVATE_TOKEN)
    gl.auth()

    # print(f"You are logged in as {gl.user.name} ({gl.user.username}) in {gl.url}")

    return gl
