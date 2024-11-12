import os.path as path
from os import getcwd, listdir


class FileExtensions:
    DOCX = ".docx"
    PPTX = ".pptx"
    XLSX = ".xlsx"
    PDF = ".pdf"


def _get_abs_path(input_path: str) -> str:
    """Resolve to absolute path based on input."""

    if path.isabs(input_path):
        abs_path = path.abspath(input_path)
    else:
        abs_path = path.abspath(path.join(getcwd(), input_path))

    return abs_path


def check_in_file(file_path: str, ext: str) -> str:
    """Check if a file exists and has the correct format."""
    abs_path = _get_abs_path(file_path)

    if not abs_path.endswith(ext):
        raise FileError(f"Wrong File Format. Provide a {ext} file.")

    if not path.isfile(abs_path):
        raise FileNotFoundError(
            f"{path.basename(abs_path)} does not exist in the specified directory."
        )

    # Check for Microsoft Office lock file (starts with ~$)
    lock_file = path.join(path.dirname(abs_path), f"~${path.basename(abs_path)[1:]}")
    if path.isfile(lock_file):
        raise IOError(
            f"{path.basename(abs_path)} is currently locked (possibly open in another application)."
        )

    return abs_path


def check_out_file(file_path: str, ext: str) -> str:
    """Check if a file can be created with the correct format."""
    abs_path = _get_abs_path(file_path)

    if not abs_path.endswith(ext):
        raise FileError(f"Wrong File Format. Provide a {ext} file.")

    if path.exists(abs_path):
        raise FileExistsError(f"{path.basename(abs_path)} already exists.")

    return abs_path


def check_dir(dir_path: str) -> str:
    """Check if a directory exists and return its absolute path."""
    abs_path = _get_abs_path(dir_path)

    if not path.isdir(abs_path):
        raise PathError(f"The specified directory '{dir_path}' is invalid or does not exist.")

    return abs_path


def files_with_suffix(directory: str, ext: str | tuple[str]) -> list[str]:
    """List all files with a specific extension in a given directory."""
    check_dir(directory)  # Ensure the directory exists
    return list(filter(lambda f: f.endswith(ext), listdir(directory)))


class FileError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return super().__str__()


class PathError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return super().__str__()
