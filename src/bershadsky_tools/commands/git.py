import os
import click
import datetime

from git import Repo

from bershadsky_tools.commands import version
from bershadsky_tools.commands.base import b8y
from bershadsky_tools import options


__all__ = [
    "git_group",
    "release",
]


@b8y.group("git")
def git_group():
    pass


@git_group.command()
@options.project_path()
@options.version_file()
def release(path, version_file):
    """
    Creates release tag and push it to repository according to version file
    """
    from bershadsky_tools.commands.version import current

    ctx = click.get_current_context()
    current_version = ctx.invoke(current, version_file=version_file, quiet=True)

    repository = Repo(path)

    if repository.is_dirty():
        click.confirm("Repository is not committed, proceed?", abort=True)
        commit_message = click.prompt("Committing, please enter commit message")
        repository.git.commit("-a", "-m", commit_message)

    tags = {i.name for i in sorted(repository.tags, key=lambda i: i.commit.authored_date)}

    if current_version in tags:
        click.confirm(f"Current tag ({current_version}) exists, proceed?", abort=True)

    click.confirm(f"You are about to release ({current_version}) tag, proceed?", abort=True)

    repository.git.tag("-f", current_version)


@git_group.command()
@options.project_path()
def push_tags(path):
    repository = Repo(path)
    repository.git.push("--tags")


@git_group.command()
@options.project_path()
def changelog(path):
    """
    Generated changelog grouping by date, version tag and lists comments
    """

    if not os.path.exists(os.path.join(os.getcwd(), '.git')):
        raise click.BadParameter("Not a git repository. Impossible to create changelog file")

    repository = Repo(path)
    tags = {}

    for tag in repository.tags:
        tags.setdefault(tag.commit, str(tag))

    prev_tag = None
    current_tag = click.get_current_context().invoke(version.current, path=path, quiet=True)
    result = ["# Change log"]

    add = lambda s: result.append(s)
    for commit in repository.iter_commits():
        committed = datetime.datetime.fromtimestamp(commit.committed_date, datetime.timezone.utc)
        current_tag = tags.get(commit) or current_tag
        if current_tag != prev_tag:
            add("") if result else None
            add(f"**{current_tag} - {committed.strftime('%Y-%m-%d')}**")
            prev_tag = current_tag

        add(f"- {commit.author}: {commit.summary}")

    result = '\n'.join(result)

    with open("CHANGELOG.md", "w+") as h:
        h.write(result)
