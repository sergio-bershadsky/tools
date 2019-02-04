import click
import functools


sh_out = functools.partial(click.echo, nl=False)
