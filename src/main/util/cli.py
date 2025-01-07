import warnings

import click

from src.main.util import chat_cli, rag_loader


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


@ws.command(help="Run CLI chat using the specified RAG module")
@click.argument("module-name", type=click.Choice(rag_loader.get_names()), required=True)
def run(module_name: str):
    chain = rag_loader.load_chain(module_name)
    chat_cli.run(chain)


@ws.command(help="Run GUI")
def gui():
    import subprocess
    from tabulate import tabulate

    command = ["chainlit", "run", "src/main/util/chat_gui.py", "--watch"]
    click.echo()
    click.echo(tabulate(
        tabular_data=[
            ["Launching Chainlit web UI in a subprocess."],
            [f"#ProTip: You can also debug if you set up your IDE to execute `{" ".join(command)}` as a Python process "
             f"and run that instead."]
        ],
        tablefmt="rst"
    ))
    subprocess.run(command)


# TODO
@ws.command(help="Run evaluations specific to the current version")
def evals():
    click.echo(
        "Evaluating like this is not currently supported, please execute the python scripts from the repo root instead."
    )
