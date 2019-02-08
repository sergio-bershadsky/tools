import click
import functools


out = functools.partial(click.echo, nl=False)
