import click
import functools


click.option = functools.partial(click.option, show_default=True)
click.option = functools.partial(click.option, show_envvar=True)


from bershadsky_tools.commands.base import *
from bershadsky_tools.commands.git import *
from bershadsky_tools.commands.python import *
from bershadsky_tools.commands.version import *


def main():
    b8y(auto_envvar_prefix='TOOLS')


if __name__ == '__main__':
    main()
