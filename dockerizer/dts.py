import os
import click 

@click.group()
def cli():
    """
    Try `dts {command-name} --help for more help
    """
    pass


@cli.command()
def cleanup():
    """
    Deletes docker images/containers and removes related files
    """
    click.echo("Temporarily not implemented")


@cli.command()
@click.option(
    "--base", 
    "-b", 
    type=click.STRING,
    required=True,
    help="Base image for docker container",
)
def init(base):
    """
    Initializes all docker configuration files
    """
    click.echo(f"current dir: {os.getcwd()}")