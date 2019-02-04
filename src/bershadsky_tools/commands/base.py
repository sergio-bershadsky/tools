import sh
import click

from bershadsky_tools import utils


__all__ = [
    "b8y",
    "update",
]


@click.group("b8y")
def b8y():
    pass


@b8y.command()
def update():
    sh.pip.install(
        "git+https://github.com/sergio-bershadsky/tools.git",
        _out=utils.sh_out
    )
