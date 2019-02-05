import functools
import os
import re
import click

from git import Repo
from sh import git

from bershadsky_tools.commands.base import b8y
from bershadsky_tools import options, utils

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
        click.confirm("Repository is not committed, proceed?")
        commit_message = click.prompt("Committing, please enter commit message")
        repository.git.commit("-a", "-m", commit_message)

    tags = {i.name for i in sorted(repository.tags, key=lambda i: i.commit.authored_date)}

    if current_version in tags:
        click.confirm(f"Current tag ({current_version}) exists, proceed?", abort=True)

    repository.git.tag("-f", current_version)


@git_group.command()
@options.project_path()
def changelog(path):
    """
    Generated changelog grouping by date, version tag and lists comments
    """

    if not os.path.exists(os.path.join(path, '.git')):
        raise click.BadParameter("Not a git repository. Impossible to create changelog file")

    tag_dates = git.log('--no-walk', '--tags', '--date=short', '--pretty="%d %ai"')\
        .replace('"', '')\
        .split('\n')

    # unique & not empty
    uniques_tag_dates = [
        # extract tagname & fulldate & split them
        re.sub(r'.*tag: ([a-z0-9.]+).*\) (.+)',  r'\1 \2', td).split(' ', 1) for td in set(filter(None, tag_dates))
    ]
    sorted_tag_dates = sorted(uniques_tag_dates, key=lambda td: td[1], reverse=True)

    changelog_file = os.path.join(path, 'CHANGELOG.md')
    with open(changelog_file, 'w') as h:
        for index, td in enumerate(sorted_tag_dates):
            tag, date = td
            try:
                _, date_next = sorted_tag_dates[index+1]
            except IndexError:
                date_next = None

            if date_next:
                messages = git.log('--no-merges',
                                   '--pretty=" - **%aN**%<|(40)%x3A_%s_"',
                                   '--since=' + date_next,
                                   '--until=' + date,
                                   '--all') \
                    .replace('"', '') \
                    .split('\n')

                # until include message from previous tag
                messages = messages[:-2]
            else:
                # first block
                messages = git.log('--no-merges',
                                   '--pretty=" - **%aN**%<|(40)%x3A_%s_"',
                                   '--until=' + date,
                                   '--all') \
                    .replace('"', '') \
                    .split('\n')

                messages = messages[:-1]

            if len(messages):
                h.write("### [{}] - {}\n".format(tag, date.split(' ', 1)[0]))

                h.writelines(map(lambda x: x + '\n', messages))
                h.write('\n')

    click.echo("Done")
