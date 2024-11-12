import threading
from datetime import timedelta
from functools import wraps
from itertools import cycle
from time import sleep, time
from typing import Callable, Iterator

from click import secho

from .utils import SPINNER, Colors, Cursors


def _spin(msg: str, start_time: float, frames: Iterator[str], _stop_spin: threading.Event):
    """Updates the spinner animation in its own thread"""
    DELAY = 0.1
    while not _stop_spin.is_set():
        # Calculate elapsed time components once
        elapsed_time = time() - start_time
        sec, fsec = divmod(round(100 * elapsed_time), 100)
        formatted_time = f"  {msg} : {timedelta(seconds=sec)}.{fsec:02.0f}"

        # Update spinner frame
        frame = next(frames) + formatted_time
        secho(f"\r{frame}", fg=Colors.YELLOW, bold=True, nl=False)
        sleep(DELAY)


def spinner(msg: str = "Elapsed Time"):
    """
    Decorator that displays a colored spinner with a message while the main functions is executed

        Args:
            msg: Message displayed with the spinner
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper_decorator(*args, **kwargs):
            # Setup spinner thread
            _stop_spin = threading.Event()
            start_time = time()

            _spin_thread = threading.Thread(
                target=_spin, args=(msg, start_time, cycle(SPINNER), _stop_spin)
            )
            _spin_thread.start()

            try:
                # Execute the wrapped function
                result = func(*args, **kwargs)
                secho(f"\r{Cursors.CHECKMARK}  {msg}", fg=Colors.GREEN, bold=True)
                return result

            except Exception as e:
                # Handle errors
                secho(f"\r{Cursors.EXIT_CURSOR}  {msg}", fg=Colors.RED, bold=True)
                error_msg = f"\nError occurred: {e}\n" f"Exception Type: {type(e).__name__}\n"
                secho(error_msg, fg="red")
                return None

            finally:
                # Stop the spinner thread
                _stop_spin.set()
                _spin_thread.join()

        return wrapper_decorator

    return decorator
