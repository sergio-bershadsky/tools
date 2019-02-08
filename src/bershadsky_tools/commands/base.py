import sh
import click

from bershadsky_tools import utils


__all__ = [
    "b8y",
    "update",
]


def version_callback(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    import bershadsky_tools

    click.echo(bershadsky_tools.__version__)
    ctx.exit()


@click.group("b8y")
@click.option(
    '--version', is_flag=True, callback=version_callback, expose_value=False, is_eager=True,
    help="Print version and exit"
)
def b8y():
    pass


@b8y.command()
def update():
    sh.pip.install(
        "git+https://github.com/sergio-bershadsky/tools.git",
        _out=utils.sh_out
    )
