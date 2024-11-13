import warnings

import click

from src.main.util import git


@click.group(
    name="ws",
    context_settings={'show_default': True},
    help="The CLI for RAG: Beyond The Basics."
)
def ws():
    pass


@ws.command(help="Test if the CLI works and dependencies can be imported")
def hello():
    try:
        click.echo(f"Checking some things...")
        warnings.filterwarnings("ignore", category=Warning, message=".*deepeval.*")
        import deepeval, langchain, langgraph
        click.echo(f"Seems like everything works so far!")
        click.echo(f"Make sure you also have your LangSmith API key ready for the workshop.")
        click.echo(f"See you on Wednesday at 6PM here: https://maps.app.goo.gl/bjTNDQyu64id73m97")
    except:
        click.echo("The CLI works, but we can't import dependencies :/", err=True)


@ws.command(help="Run the RAG script")
def run():
    click.echo(
        "Running like this is not currently supported, please execute the python scripts from the repo root instead.")


@ws.command(help="Run evaluations specific to the current version")
def evals():
    click.echo(
        "Evaluating like this is not currently supported, please execute the python scripts from the repo root instead.")


@ws.command(help="Print your current active version")
def where():
    _print_version()


@ws.command(help="Step to the next version")
def next():
    git.goto_next()
    _print_version()


@ws.command(help="Step to the previous version")
def prev():
    git.goto_previous()
    _print_version()


@ws.command(help="Go to the version you specify")
@click.argument("version", type=str, required=True)
def goto(version: str):
    git.goto(version)
    _print_version()


def _print_version():
    commit_message = git.get_version()
    click.echo(f"You are currently on version {commit_message}.")
