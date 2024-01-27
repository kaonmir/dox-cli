import click
import gitlab
import os
import requests


def load_gitlab(GITLAB_URL, GITLAB_PRIVATE_TOKEN):
    if not GITLAB_URL:
        raise click.ClickException("GITLAB_URL not set")
    if not GITLAB_PRIVATE_TOKEN:
        raise click.ClickException("GITLAB_PRIVATE_TOKEN not set")

    try:
        timeout_duration = 2
        requests.get(GITLAB_URL, timeout=timeout_duration)
    except requests.exceptions.ConnectionError:
        raise Exception(f"Unable to connect to {GITLAB_URL}")

    gl = gitlab.Gitlab(GITLAB_URL, GITLAB_PRIVATE_TOKEN)
    gl.auth()

    # print(f"You are logged in as {gl.user.name} ({gl.user.username}) in {gl.url}")

    return gl
