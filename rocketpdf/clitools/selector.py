from typing import Optional

from click import echo, getchar, secho, style

from .utils import DISABLE_BLINK, ENABLE_BLINK, Colors, Cursors, clear_lines

# Helper Text
EXIT_TEXT = "Quit (q)"
HELP_TEXT = "[↑/k] up | [↓/j] down | [enter] select | [q] quit"


def prompter(prompt: str, choices: list[str]) -> Optional[str]:
    """
    Display an interactive prompt with selectable options.

    Args:
        prompt: Text to display above the options
        choices: List of options to choose from
    """
    if not choices:
        raise ValueError("Options list must contain at least one item.")

    if not all(choice != "" for choice in choices):
        raise ValueError("Options list cannot be empty strings")

    secho(prompt, fg=Colors.YELLOW)

    selection = _select_option(choices)

    # Reprints the selected option next to the prompt
    clear_lines()
    secho(prompt, fg=Colors.YELLOW, nl=False)

    if selection:
        echo(selection.split(maxsplit=1)[0])

    return selection


# TODO: Reduce flickering updating only the updated lines current_row and prev_row
def _display_menu(options: list[str], current_row: int) -> str:
    """Updates the current menu to be displayed according to the cursor position."""
    display_text = ""

    for i, option in enumerate(options):
        # Highlight selected row with green [selected], red [exit] or white [non-selected]
        if i == current_row:
            prefix = Cursors.EXIT_CURSOR if option == EXIT_TEXT else Cursors.SELECTED
            sel_color = Colors.RED if option == EXIT_TEXT else Colors.GREEN
            display_text += style(f"{prefix} {option}\n", fg=sel_color, bold=True)
        else:
            display_text += style(f"{Cursors.NON_SELECTED} {option}\n", fg=Colors.WHITE)

    # Display help text
    display_text += style(HELP_TEXT, fg=Colors.MAGENTA, dim=True)
    return display_text


def _select_option(options: list[str]) -> Optional[str]:
    """Handle user keydown presses for navigating options."""
    # Create a copy of the list with the quit option
    menu_options = options + [EXIT_TEXT]
    current_row = 0

    # Disable cursor blink
    echo(DISABLE_BLINK, nl=False)

    # Initial display
    echo(_display_menu(menu_options, current_row))

    try:
        while True:
            ch = getchar()

            match ch:
                # WIN ARROW UP KEY | UNIX ARROW UP KEY | VIM UP KEY
                case "\xe0H" | "\x1b[A" | "k":
                    if current_row == 0:
                        continue
                    current_row = current_row - 1
                    current_menu = _display_menu(menu_options, current_row)
                    clear_lines(len(menu_options))
                    echo(current_menu)

                # WIN ARROW DOWN KEY | UNIX ARROW DOWN KEY | VIM DOWN KEY
                case "\xe0P" | "\x1b[B" | "j":
                    if current_row == len(options):
                        continue
                    current_row = current_row + 1
                    current_menu = _display_menu(menu_options, current_row)
                    clear_lines(len(menu_options))
                    echo(current_menu)

                # ENTER KEY
                case "\r" | "\n":
                    selected = menu_options[current_row]
                    if selected == EXIT_TEXT:
                        selected = None
                    break

                # EXIT
                case "q":
                    selected = None
                    break

    # Handle Ctrl+C exit gracefully
    except KeyboardInterrupt:
        selected = None

    clear_lines(len(menu_options))

    # Re-enable cursor blink
    echo(ENABLE_BLINK, nl=False)

    return selected
