import warnings

import click


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
    click.echo(f"You want to run the RAG script.")


@ws.command(help="Run evaluations")
@click.option(
    "--all", type=bool, is_flag=True, default=False,
    help="Whether to run all evaluations or only some",
    show_default="Only run evaluations specific to the current version"
)
def evals(all: bool):
    if all:
        click.echo(f"You want to run all evaluations.")
    else:
        click.echo(f"You want to run some evaluations.")


@ws.command(help="Print your current active version")
def where():
    click.echo(f"You want to know which version you're currently on.")


@ws.command(help="Step to the next version")
def next():
    click.echo(f"You want to switch to the next version.")


@ws.command(help="Step to the previous version")
def prev():
    click.echo(f"You want to switch to the previous version.")


@ws.command(help="Go to the version you specify")
@click.argument("version", type=str, required=True)
def goto(version: str):
    click.echo(f"You want to switch to version {version}.")
