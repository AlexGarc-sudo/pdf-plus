from click import echo


class Colors:
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    WHITE = "white"
    MAGENTA = "bright_magenta"


class Cursors:
    SELECTED = "→"
    NON_SELECTED = " "
    EXIT_CURSOR = "✕"
    CHECKMARK = "✓"


SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"  # Sequence of spinner frames used in the spinner animation.

CURSOR_UP = "\033[1A"  # ANSI escape sequence to move cursor up one line
CLEAR_LINE = "\033[K"  # ANSI escape sequence to clear the current line
DISABLE_BLINK = "\033[?12l"  # Disable cursor blinking in terminal
ENABLE_BLINK = "\033[?12h"  # Re-enable cursor blinking in terminal


def clear_lines(n_lines: int = 0) -> None:
    """Clears the terminals n lines up"""
    clear_text = f"{CURSOR_UP}{CLEAR_LINE}" * (n_lines + 1)  # +1 for help text
    echo(clear_text, nl=False)
