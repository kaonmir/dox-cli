import click
from dox.utils.gitlab import load_gitlab
from dox.utils.helpers import open_structured_file
from gitlab.exceptions import GitlabCreateError
import re


def iter_groups(root, namespace=[]):
    for root_name, children in root.items():
        if not match_group_route_regex(root_name):
            raise click.ClickException(f"Group name {root_name} is not valid. Please check the group name")

        namespace.append(root_name)
        if isinstance(children, dict):
            # root has children groups
            yield namespace
            yield from iter_groups(children, namespace)
        elif children == None:
            # root has no children
            yield namespace
        else:
            raise click.ClickException("groups yaml is not allowed to have list")

        namespace.pop()


def match_group_route_regex(group_name):
    r = "(?:[a-zA-Z0-9_\.][a-zA-Z0-9_\-\.]{0,38})"
    return re.fullmatch(r, group_name) is not None
    # return ValueError(f"Group name {group_name} is not valid. Please check the group name")


def match_full_namespace_format_regex(name):
    r = r"(?:(?:[a-zA-Z0-9_\.][a-zA-Z0-9_\-\.]{0,38}[a-zA-Z0-9_\-]|[a-zA-Z0-9_])\/){0,20}(?:[a-zA-Z0-9_\.][a-zA-Z0-9_\-\.]{0,38}[a-zA-Z0-9_\-]|[a-zA-Z0-9_])"
    return re.fullmatch(r, name) is not None


@click.option(
    "--gitlab-url",
    default="https://gitlab.com",
    metavar="URL",
    envvar="GITLAB_URL",
)
@click.option(
    "--gitlab-private-token",
    envvar="GITLAB_PRIVATE_TOKEN",
    metavar="TOKEN",
    required=True,
)
@click.argument("filename", type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.command()
def create_group(gitlab_url, gitlab_private_token, filename):
    """Create bulk groups

    \b
    You can create a group hierarchy by using a yaml file.
    Group always starts with root group and ends with null.

    \b
    Example yaml file:

    \b
    root_group:
      sub_group:
        sub_sub_group: null
    """

    groups = open_structured_file(filename)
    if groups == None:
        raise ValueError(f"File {filename} is empty")

    gl = load_gitlab(gitlab_url, gitlab_private_token)

    for namespace in iter_groups(groups):
        namespace_str = "/".join(namespace)
        try:
            group = gl.groups.get(namespace_str)
            # Group exists
            click.echo(f"exist: {namespace_str}")
        except Exception as e:
            # Group does not exist
            try:
                if len(namespace) == 1:
                    # Create root group
                    if gitlab_url == "https://gitlab.com":
                        raise click.ClickException(
                            f"Root group can not be created programmatically in gitlab.com. Please create root group manually."
                        )
                    group = gl.groups.create({"name": namespace[-1], "path": namespace[-1]})
                else:
                    # create sub group
                    parent_group = gl.groups.get("/".join(namespace[:-1]))
                    group = gl.groups.create(
                        {
                            "parent_id": parent_group.id,
                            "name": namespace[-1],
                            "path": namespace[-1],
                        }
                    )
                click.echo(f"created: {namespace_str}")

            except GitlabCreateError as e:
                raise click.ClickException(
                    f"Group name {namespace[-1]} may already be taken by someone. Or you may not have permission to create group {namespace_str}"
                )
            except Exception as e:
                raise click.ClickException(f"Group creation failed. {e}")


# return value is namespaces and is_group
if __name__ == "__main__":
    create_group(["./test/group.yml"])

    # path_regex = GitlabPathRegex()
    # print(path_regex.FULL_NAMESPACE_FORMAT_REGEX)

    # for group in iter_groups(open_structured_file("./test/group.yml")):
    #     print(group)
