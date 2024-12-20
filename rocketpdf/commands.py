import inspect
from typing import Optional

import click

from .clitools import Colors
from .rocketpdf import docx_to_pdf
from .utils.path import handle_input, handle_output


class Extensions:
    DOCX = ".docx"
    PPTX = ".pptx"
    XLSX = ".xlsx"
    PDF = ".pdf"


class Commands:
    """Contains the list of commands to execute"""

    def __init__(self, group: click.Group):
        self.commands = {}

        for name, command in inspect.getmembers(self):
            if isinstance(command, click.Command):
                group.add_command(command)
                self.commands[name] = command

    def __description__(self) -> list[str]:
        # Find longest command name for padding
        max_name_length = max(len(cmd.name) for cmd in self.commands.values())

        # Format: "command    description"
        def format_command(cmd: click.Command) -> str:
            return f"{cmd.name:<{max_name_length}}    {cmd.callback.__doc__}"

        formatted_commands = list(map(format_command, self.commands.values()))

        return formatted_commands

    # rocketpdf commands

    @click.command()
    @click.argument("input", type=click.Path(exists=True, resolve_path=True), required=False)
    @click.option("-o", "--output", type=click.Path())
    def parsedoc(input: Optional[str] = None, output: Optional[str] = None):
        """Convert DOCX to PDF."""

        try:
            if not input:
                input = handle_input(Extensions.DOCX)

            output = handle_output(output, input, Extensions.PDF)
        except (FileNotFoundError, ValueError, IOError) as e:
            click.secho(str(e), fg=Colors.RED)
            click.secho("Aborting...", fg=Colors.RED)
            return

        return docx_to_pdf(input, output)
