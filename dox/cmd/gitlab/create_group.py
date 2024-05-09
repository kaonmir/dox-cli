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
        if isinstance(children, str):
            # Project
            branch_name = children
            yield namespace, branch_name
        elif isinstance(children, dict):
            # root has children groups
            yield namespace, None
            yield from iter_groups(children, namespace)
        elif children == None:
            # root has no children
            yield namespace, None
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
    gitlab_private_token = "glpat-rUEfy6kfP4yKN5ShtMBM"
    gitlab_url = "https://gitlab.dev.labs.infograb.io"

    """Create bulk groups

    \b
    You can create a group hierarchy by using a yaml file.
    Group/Project always starts with root group and ends with the desired default branch name.
    Every leaf node is a project and every other node is a group.

    \b
    Example yaml file:

    \b
    root_group:
      sub_group:
        sub_sub_group: main
    """

    groups = open_structured_file(filename)
    if groups == None:
        raise ValueError(f"File {filename} is empty")

    gl = load_gitlab(gitlab_url, gitlab_private_token)

    for namespace_arr, branch in iter_groups(groups):
        namespace_str = "/".join(namespace_arr)
        # Case 1: Project
        if branch != None:
            try:
                project = gl.projects.get(f"{namespace_str}")
                # Case 1.1: Project exists
                click.echo(f"exist: {namespace_str}")
            except Exception as e:
                # Case 1.2: Project does not exist, so create it
                try:
                    parent_namespace = gl.namespaces.get("/".join(namespace_arr[:-1]))
                    project = gl.projects.create(
                        {
                            "name": namespace_arr[-1],
                            "namespace_id": parent_namespace.id,
                            "default_branch": branch,
                            "initialize_with_readme": False,
                        }
                    )
                    click.echo(f"created: {namespace_str} on {branch} branch")
                except GitlabCreateError as e:
                    raise click.ClickException(
                        f"Project name {namespace_arr[-1]} may already be taken by someone. Or you may not have permission to create project {namespace_str}"
                    )
                except Exception as e:
                    raise click.ClickException(f"Project creation failed. {e}")
        # Case 2: Group
        else:
            # Case 2.1: Group exists
            try:
                group = gl.groups.get(namespace_str)
                click.echo(f"exist: {namespace_str}")
            # Case 2.2: Group does not exist, so create it
            except Exception as e:
                try:
                    # Case 2.2.1 Create root group
                    if len(namespace_arr) == 1:
                        if gitlab_url == "https://gitlab.com":
                            raise click.ClickException(
                                f"Root group can not be created programmatically in gitlab.com. Please create root group manually."
                            )
                        group = gl.groups.create({"name": namespace_arr[-1], "path": namespace_arr[-1]})
                    # 2.2.2: create sub group
                    else:
                        parent_group = gl.groups.get("/".join(namespace_arr[:-1]))
                        group = gl.groups.create(
                            {
                                "parent_id": parent_group.id,
                                "name": namespace_arr[-1],
                                "path": namespace_arr[-1],
                            }
                        )
                    click.echo(f"created: {namespace_str}")

                except GitlabCreateError as e:
                    raise click.ClickException(
                        f"Group name {namespace_arr[-1]} may already be taken by someone. Or you may not have permission to create group {namespace_str}"
                    )
                except Exception as e:
                    raise click.ClickException(f"Group creation failed. {e}")


# return value is namespaces and is_group
if __name__ == "__main__":
    create_group(
        "https://gitlab.dev.labs.infograb.io",
        "",
        "/Volumes/Code/kaonmir/dox-cli/test/hcs.yml",
    )

    # path_regex = GitlabPathRegex()
    # print(path_regex.FULL_NAMESPACE_FORMAT_REGEX)

    # for group in iter_groups(open_structured_file("./test/group.yml")):
    #     print(group)
