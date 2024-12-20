from platform import system
from typing import Protocol


class ConverterEngine(Protocol):
    """
    Protocol defining a converter engine interface for file type conversions.

    This interface specifies methods for converting between various file formats.
    Implementing classes should provide the functionality to convert:
    - DOCX files to PDF format.
    - PDF files to DOCX format.

    """

    def docx_to_pdf(self, input_file: str, output_file: str) -> None: ...

    def pdf_to_docx(self, input_file: str, output_file: str) -> None: ...


def get_local_engine() -> ConverterEngine:
    """Returns the default converting engine based on the operating system used"""
    op_s = system()
    match op_s:
        case "Windows":
            from .win32 import WindowsConverterEngine

            return WindowsConverterEngine()
        case "Linux":
            from .linux import LinuxConverterEngine

            return LinuxConverterEngine()
        case "Darwin":
            from .darwin import DarwinConverterEngine

            return DarwinConverterEngine()
        case _:
            raise NotImplementedError(f"Unsupported Operating System: {op_s}")


LOCAL_ENGINE = get_local_engine
