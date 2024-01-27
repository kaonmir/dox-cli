import re


class GitlabPathRegex:
    # Constants
    TOP_LEVEL_ROUTES = [
        "-",
        ".well-known",
        "404.html",
        "422.html",
        "500.html",
        "502.html",
        "503.html",
        "admin",
        "api",
        "apple-touch-icon.png",
        "assets",
        "dashboard",
        "deploy.html",
        "explore",
        "favicon.ico",
        "favicon.png",
        "files",
        "groups",
        "health_check",
        "help",
        "import",
        "jwt",
        "login",
        "oauth",
        "profile",
        "projects",
        "public",
        "robots.txt",
        "s",
        "search",
        "sitemap",
        "sitemap.xml",
        "sitemap.xml.gz",
        "slash-command-logo.png",
        "snippets",
        "unsubscribes",
        "uploads",
        "users",
        "v2",
    ]

    PROJECT_WILDCARD_ROUTES = [
        "-",
        "badges",
        "blame",
        "blob",
        "builds",
        "commits",
        "create",
        "create_dir",
        "edit",
        "environments/folders",
        "files",
        "find_file",
        "gitlab-lfs/objects",
        "info/lfs/objects",
        "new",
        "preview",
        "raw",
        "refs",
        "tree",
        "update",
        "wikis",
    ]

    GROUP_ROUTES = ["-"]

    ILLEGAL_PROJECT_PATH_WORDS = PROJECT_WILDCARD_ROUTES
    ILLEGAL_GROUP_PATH_WORDS = list(set(PROJECT_WILDCARD_ROUTES + GROUP_ROUTES))
    ILLEGAL_ORGANIZATION_PATH_WORDS = list(set(TOP_LEVEL_ROUTES + PROJECT_WILDCARD_ROUTES + GROUP_ROUTES))

    PATH_START_CHAR = "[a-zA-Z0-9_\.]"
    PATH_REGEX_STR = PATH_START_CHAR + "[a-zA-Z0-9_\-\.]" + "{0,38}"
    NAMESPACE_FORMAT_REGEX_JS = PATH_REGEX_STR + "[a-zA-Z0-9_\-]|[a-zA-Z0-9_]"

    NO_SUFFIX_REGEX = "(?<!\\.git|\\.atom)"
    NAMESPACE_FORMAT_REGEX = f"(?:{NAMESPACE_FORMAT_REGEX_JS}){NO_SUFFIX_REGEX}"
    PROJECT_PATH_FORMAT_REGEX = f"(?:{PATH_REGEX_STR}){NO_SUFFIX_REGEX}"
    FULL_NAMESPACE_FORMAT_REGEX = f"({NAMESPACE_FORMAT_REGEX}/){{,20}}{NAMESPACE_FORMAT_REGEX}"

    # Methods
    def organization_route_regex(self):
        illegal_words = re.compile("|".join(self.ILLEGAL_ORGANIZATION_PATH_WORDS), re.IGNORECASE)
        return f"(?!(?:{illegal_words})/){self.NAMESPACE_FORMAT_REGEX}"

    def root_namespace_route_regex(self):
        illegal_words = re.compile("|".join(self.TOP_LEVEL_ROUTES), re.IGNORECASE)
        return f"(?!(?:{illegal_words})/){self.NAMESPACE_FORMAT_REGEX}"

    def full_namespace_route_regex(self):
        illegal_words = re.compile("|".join(self.ILLEGAL_GROUP_PATH_WORDS), re.IGNORECASE)
        return (
            f"{self.root_namespace_route_regex()}/(?:/(?!(?:{illegal_words})/){self.NAMESPACE_FORMAT_REGEX})*"
        )

    def project_route_regex(self):
        illegal_words = re.compile("|".join(self.ILLEGAL_PROJECT_PATH_WORDS), re.IGNORECASE)
        return f"(?!(?:{illegal_words})/){self.PROJECT_PATH_FORMAT_REGEX}"

    def repository_route_regex(self):
        return f"({self.full_namespace_route_regex()}|{self.personal_snippet_repository_path_regex()})\./*"

    def repository_git_route_regex(self):
        return f"{self.repository_route_regex()}\\.git"

    def repository_git_lfs_route_regex(self):
        return f"{self.repository_git_route_regex()}/(info/lfs|gitlab-lfs)/"

    def repository_wiki_git_route_regex(self):
        return f"{self.full_namespace_route_regex()}.*\\.wiki\\.git"

    def full_namespace_path_regex(self):
        return f"^{self.full_namespace_route_regex()}/$"

    def organization_path_regex(self):
        return f"^{self.organization_route_regex()}/$"

    def full_project_path_regex(self):
        return f"^{self.full_namespace_route_regex()}/{self.project_route_regex()}/$"

    def full_project_git_path_regex(self):
        return f"^/?{self.full_namespace_route_regex()}/{self.project_route_regex()}\\.git$"

    def namespace_format_regex(self):
        return f"^{self.NAMESPACE_FORMAT_REGEX}$"

    def namespace_format_message(self):
        return (
            "can contain only letters, digits, '_', '-' and '.'. "
            "Cannot start with '-' or end in '.', '.git' or '.atom'."
        )

    def project_path_format_regex(self):
        return f"^{self.PROJECT_PATH_FORMAT_REGEX}$"

    def project_path_format_message(self):
        return (
            "can contain only letters, digits, '_', '-' and '.'. "
            "Cannot start with '-', end in '.git' or end in '.atom'."
        )

    def archive_formats_regex(self):
        return r"(zip|tar|tar\.gz|tgz|gz|tar\.bz2|tbz|tbz2|tb2|bz2)"

    def git_reference_regex(self):
        return r"(?!(?:/|.*(?:[\/.]\.|\/\/|@\{|\\\\)))[^\000-\040\177~^:?*\[]+" r"(?<!\.lock)(?<![\/.])"

    def full_snippets_repository_path_regex(self):
        return f"^({self.personal_snippet_repository_path_regex()}|{self.project_snippet_repository_path_regex()})$"

    def container_image_regex(self):
        return r"([\w\.-]+\/){0,4}[\w\.-]+"

    def container_image_blob_sha_regex(self):
        return r"[\w+.-]+:?\w+"

    def dependency_proxy_route_regex(self):
        return f"^/v2/{self.full_namespace_route_regex()}/dependency_proxy/containers/{self.container_image_regex()}/(manifests|blobs)/{self.container_image_blob_sha_regex()}$"

    # Helper methods for regexes that depend on other regexes
    def personal_snippet_repository_path_regex(self):
        return f"{self.personal_snippet_path_regex()}/\\d+"

    def personal_snippet_path_regex(self):
        return r"snippets"

    def project_snippet_repository_path_regex(self):
        return f"{self.project_snippet_path_regex()}/\\d+"

    def project_snippet_path_regex(self):
        return f"{self.full_namespace_route_regex()}/{self.project_route_regex()}/snippets"
