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
        click.echo(
            f"Python modules loaded, dependencies can be imported: things seems to work. See you at the workshop!")
    except:
        click.echo("The CLI works, but we can't import dependencies :/", err=True)


@ws.command(help="Chat on the command line with the specified RAG_MODULE")
@click.argument("rag-module", type=click.Choice(rag_loader.get_names()), required=False)
def cli(rag_module: str):
    if not rag_module:
        rag_module = click.prompt("Specify RAG module", type=click.Choice(rag_loader.get_names()))
    chain = rag_loader.load_chain(rag_module)
    chat_cli.run(chain)


@ws.command(help="Start RAG chat in the browser UI")
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

# TODO: Implement
#  - Let suites take chain as arg
#  - This takes argument rag_module, option --full
#  - Choose suite, inject chain, run
# @ws.command(help="Run evaluation suite for the specified RAG_MODULE")
# def test():
#     click.echo(
#         "Evaluating like this is not currently supported, please execute the python scripts from the repo root instead."
#     )
