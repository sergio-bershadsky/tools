import os
import click
import semver

from bershadsky_tools.commands.base import b8y
from bershadsky_tools import options


__all__ = [
    "version_group",
    "semver_command",
    "current",
]


@b8y.group("version")
def version_group(**options):
    pass


@version_group.command("semver")
@click.argument(
    "bump", type=click.Choice(["init", "major", "minor", "patch", "pre"]), default="patch"
)
@click.argument(
    "prerelease_name", default=None, required=False
)
@options.project_path()
@options.version_file()
@click.option(
    "--version-initial", default="0.0.0"
)
def semver_command(bump, prerelease_name, path, version_file, version_initial, **options):
    """
    Bump version to specified level [init, major, minor, patch]
    Other keyword will create pre-release version

    :param options:
    :return:
    """

    ctx = click.get_current_context()

    # Check version file exists
    current_version = ctx.invoke(current, path=path, version_file=version_file, quiet=True)

    version = current_version or version_initial
    if bump == "major":
        version = semver.bump_major(version)
    elif bump == "minor":
        version = semver.bump_minor(version)
    elif bump == "patch":
        version = semver.bump_patch(version)
    elif bump == "pre":
        version = semver.bump_prerelease(version, prerelease_name)

    # Handle pre-release with other than pre bump
    if bump != "pre" and prerelease_name:
        version = semver.bump_prerelease(version, prerelease_name)

    click.confirm(f"You are going to bump version \"{version}\", proceed?", default=True, abort=True)

    # Write version
    with open(version_file, "w+") as h:
        h.write(version)


@version_group.command()
@options.project_path()
@options.version_file()
def current(path, version_file, quiet=False):
    if not os.path.exists(version_file):
        raise click.ClickException(f"Unknown ({version_file} file does not exist)")
    else:
        with open(version_file) as h:
            result = h.read()
            quiet or click.echo(result or f"Unknown ({version_file} file empty")
    return result


