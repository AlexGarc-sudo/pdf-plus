import inspect
from typing import Optional

import click

from .clitools import Colors, prompter
from .rocketpdf import docx_to_pdf, pdf_to_docx
from .utils import FileExtensions, check_in_file, check_out_file, files_with_suffix


class Commands:
    """"""

    def __init__(self, group: click.Group):
        self.commands = {}

        for name, command in inspect.getmembers(self):
            if isinstance(command, click.Command):
                group.add_command(command)
                self.commands[name] = command

    @click.command()
    @click.argument("input", type=click.Path(exists=True), required=False)
    @click.option("-o", "--output", type=click.Path())
    def parsedoc(input: Optional[str] = None, output: Optional[str] = None):
        """Convert DOCX to PDF."""
        # Handle input if missing
        if input is None:
            input = prompter(
                "Select file you wish to convert to pdf (current dir): ",
                files_with_suffix(".", FileExtensions.DOCX),
            )
            if input is None:
                click.secho("Aborting...", fg=Colors.RED)
                return

        output = output or input.replace(".docx", ".pdf")

        try:
            input = check_in_file(input, FileExtensions.DOCX)
            output = check_out_file(output, FileExtensions.PDF)
        except FileExistsError:
            conf = click.confirm(f"{output} already exists. Do you wish to overwrite it? ")

            if not conf:
                return

        return docx_to_pdf(input, output)

    @click.command()
    @click.argument("input", type=click.Path(exists=True))
    @click.option("-o", "--output", type=click.Path())
    def parsepdf(input: str, output: str):
        """Convert PDF to DOCX."""
        click.echo("Converting PDF to DOCX...")
        pdf_to_docx(input, output)
        click.echo("Conversion complete.")

    def _format_description(self) -> list[str]:
        # Find longest command name for padding
        max_name_length = max(len(cmd.name) for cmd in self.commands.values())

        formatted_commands = []
        for cmd in self.commands.values():
            docstring = cmd.callback.__doc__ or ""

            # Format: "command    description"
            formatted = f"{cmd.name:<{max_name_length}}    {docstring}"
            formatted_commands.append(formatted)

        return formatted_commands
