from platform import system
from typing import Protocol


class ConverterEngine(Protocol):
    """
    Protocol defining a converter engine interface for file type conversions.

    This interface specifies methods for converting between various file formats.
    Implementing classes should provide the functionality to convert:
    - DOCX files to PDF format.
    - PDF files to DOCX format.
    - PPTX files to PDF format.
    - XLSX files to PDF format (experimental).

    """

    def docx_to_pdf(self, input_file: str, output_file: str) -> None: ...

    def pdf_to_docx(self, input_file: str, output_file: str) -> None: ...

    def pptx_to_pdf(self, input_file: str, output_file: str) -> None: ...

    def xlsx_to_pdf(self, input_file: str, output_file: str) -> None: ...


def get_local_engine() -> ConverterEngine:
    match system():
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
            raise NotImplementedError(f"Unsupported Operating System: {system()}")


LOCAL_ENGINE = get_local_engine()
