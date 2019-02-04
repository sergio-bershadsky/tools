import datetime
import functools
import os
import threading
import uuid

import click
import click_spinner
import sh

from bershadsky_tools.commands.base import b8y
from bershadsky_tools import options


__all__ = [
    "python",
    "freeze"
]


@b8y.group()
def python():
    pass


@python.command()
@options.project_path()
@click.option("--backup-dir", default=".backup", help="Name of backup directory")
@click.option("--requirements-file", default="requirements.pip", help="Name of requirements file")
@click.option("--requirements-frozen-file", default="requirements.frozen.pip", help="Name of frozen requirements file")
@click.option("--base-image", default="python:3.7", help="Python version to use for freezing")
def freeze(path, backup_dir, requirements_file, requirements_frozen_file, base_image):
    """
    Freeze python requirements with clean docker environment.

    Docker required
    """
    path = path or os.getcwd()

    if not os.path.exists(os.path.join(path, requirements_file)):
        raise click.exceptions.UsageError(
            f"Requirements file does'not exist at {os.path.join(path, requirements_file)}"
        )

    date_str = datetime.datetime.utcnow().strftime("%Y%m%d%H%M")

    # Process local history
    backup_dir_abs = os.path.join(path, backup_dir)
    os.makedirs(backup_dir_abs, exist_ok=True)
    backup_from_abs = os.path.join(path, requirements_frozen_file)
    if os.path.exists(backup_from_abs):
        backup_to_abs = os.path.join(backup_dir_abs, f"{date_str}.{requirements_frozen_file}")
        click.echo(f"Perform backup `{backup_from_abs}` to `{backup_to_abs}`")
        sh.mv(
            backup_from_abs,
            backup_to_abs
        )

    unique = "freezer-{}".format(uuid.uuid4().hex)

    result = []
    log = []

    def clean_docker(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                for clean_action in (
                        functools.partial(sh.docker.rm, unique),
                        functools.partial(sh.docker.image.rm, unique)):
                    clean_action()
        return wrapper

    @clean_docker
    def freeze_coroutine():
        sh.docker.run(
            "--name", unique,
            "--entrypoint", "pip",
            "-v", f"{os.path.join(path, requirements_file)}:/tmp/requirements.pip",
            base_image,
            "install", "-r", "/tmp/requirements.pip",
            _out=log.append
        )

        sh.docker.commit(unique, unique)

        sh.docker.run(
            "--rm",
            "--entrypoint", "pip",
            unique,
            "freeze",
            _out=result.append
        )

    click.echo(f"Freezing using `{base_image}` image into `{requirements_frozen_file}`, please wait ...")
    with click_spinner.spinner():
        t = threading.Thread(target=freeze_coroutine)
        t.start()
        t.join()

    for s in log:
        click.echo(s, nl=False)

    if result:
        result = ''.join(result).strip()
        click.echo(result)
        with open(os.path.join(path, requirements_frozen_file), "w+") as f:
            f.write(result)
    else:
        click.echo("Nothing to freeze")


@python.command("tweak-version")
def tweak_version():
    """
    Replace version in python project where it should be replaced

    TBD

    """
    pass