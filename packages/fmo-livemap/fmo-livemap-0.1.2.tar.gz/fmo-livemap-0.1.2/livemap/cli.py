

import os
import click


@click.group()
def cli():
    pass

@cli.command()
@click.option("--port", "-p", default=5689)
def server(port):
    from livemap.server import run_server
    run_server(port=port)

if __name__ == '__main__':
    cli()