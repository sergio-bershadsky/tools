import os
import click
import functools


def project_path_callback(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    os.chdir(value)
    return os.getcwd()


def version_file_callback(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    path = ctx.params.get("path") or ""
    if path:
        value = os.path.join(path, value)
    return value


version_file = functools.partial(
    click.option,
    "--version-file",
    type=click.Path(writable=True, readable=True, file_okay=True),
    default=".version",
    callback=version_file_callback
)

project_path = functools.partial(
    click.option,
    "-p", "--path",
    type=click.Path(exists=True, readable=True, dir_okay=True),
    callback=project_path_callback,
    default=lambda: os.getcwd(),
    help="Project root"
)
