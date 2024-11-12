import click

from .clitools import Colors, _clear_lines, prompter
from .commands import Commands


@click.group(invoke_without_command=True)
@click.pass_context
def rpdf_cli(ctx: click.Context):
    """\033[32m🚀  Rocket fast pdf handling  🚀\033[0m\n"""

    rpdf_cli.callback.__doc__ = "\n\033[34m───────│ 🚀 RocketPDF CLI │───────\033[0m\n"

    # Select subcommand from list
    if ctx.invoked_subcommand is None:
        click.echo(rpdf_cli.callback.__doc__, nl=False)
        choice = prompter("", cli._format_description())

        if choice is None:
            _clear_lines()
            click.secho("Aborting...", fg=Colors.RED)
            return

        # Extract the function name and ignore the description and map to function
        subcommand = cli.commands[choice.split(maxsplit=1)[0]]

        ctx.invoke(subcommand, input=None)


cli = Commands(rpdf_cli)
