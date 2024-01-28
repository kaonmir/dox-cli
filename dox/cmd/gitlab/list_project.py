import click
from dox.utils.gitlab import load_gitlab


def add_hierarchy(root, namespaces):
    if len(namespaces) == 0:
        return

    namespace = namespaces[0]
    if namespace not in root:
        root[namespace] = dict()

    add_hierarchy(root[namespace], namespaces[1:])


def draw_hierarchy(tree, level, bar_status=[]):
    for index, (key, value) in enumerate(tree.items()):
        for bar in bar_status:
            if bar == True:
                print("│ ", end="")
            else:
                print("  ", end="")

        if level == 0:
            print(str(key))
        elif index == len(tree) - 1:
            print("└─" + str(key))
        else:
            print("├─" + str(key))

        if level != 0:
            bar_status.append(index != len(tree) - 1)
        draw_hierarchy(value, level + 1, bar_status)
        if level != 0:
            bar_status.pop()


@click.command()
@click.option(
    "--output",
    "-o",
    default="txt",
    help="Output format. txt or csv",
)
@click.option(
    "--membership",
    "-m",
    default=True,
    help="내가 맴버로 등록된 프로젝트만 가져옵니다",
)
@click.option(
    "--group",
    "-g",
    default=None,
    help="특정 그룹을 기준으로 하위 프로젝트를 가져옵니다",
)
@click.option(
    "--gitlab-url",
    default="https://gitlab.com",
    help="Gitlab URL",
    envvar="GITLAB_URL",
)
@click.option(
    "--gitlab-private-token",
    help="Gitlab private token",
    envvar="GITLAB_PRIVATE_TOKEN",
    prompt=True,
    required=True,
)
def list_project(output, membership, group, gitlab_url, gitlab_private_token):
    """
    List projects and print the project details based on the specified output format.
    """

    if output != "csv" and output != "txt":
        raise Exception("output must be csv or txt")

    gl = load_gitlab(gitlab_url, gitlab_private_token)

    #! membership False로 하면 내가 맴버로 등록된 프로젝트가 아니고, 전체 프로젝트를 가져옴
    if group:
        group = gl.groups.get(group)
        projects = group.projects.list(per_page=100, membership=membership, iterator=True)
    else:
        projects = gl.projects.list(per_page=100, membership=membership, iterator=True)

    projects = sorted(projects, key=lambda project: project.path_with_namespace)

    if output == "csv":
        # id, created_at, path_with_namespace, visibility, http_url_to_repo, ssh_url_to_repo, default_branch
        print("id,created_at,path_with_namespace,visibility,http_url_to_repo,ssh_url_to_repo,default_branch")
        for project in projects:
            print(
                f"{project.id},{project.created_at},{project.path_with_namespace},{project.http_url_to_repo},{project.ssh_url_to_repo},{project.default_branch}"
            )

    elif output == "txt":
        tree = dict()
        for project in projects:
            namespaces = [name.strip() for name in project.path_with_namespace.split("/")]
            add_hierarchy(tree, namespaces)

        draw_hierarchy(tree, 0)
