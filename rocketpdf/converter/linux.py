import subprocess
from shutil import which
from typing import Literal

FILE_EXT = Literal["pdf", "docx"]


class LinuxConverterEngine:
    def __init__(self):
        if not self._is_libreoffice_installed():
            raise EnvironmentError("LibreOffice is not installed on this system. ")

        if not self._is_unoconv_installed():
            raise EnvironmentError("Unoconv is not installed. Install with: pip3 install unoconv")

    def _convert(self, input_file: str, output_file: str, target_format: FILE_EXT) -> None:
        """Generic conversion function using unoconv."""
        try:
            # Using `-f` to specify the format and `-o` to specify the output directory.
            subprocess.run(
                ["unoconv", "-f", target_format, "-o", output_file, input_file],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Conversion failed: {e}")

    def docx_to_pdf(self, input_file: str, output_file: str) -> None:
        """Convert DOCX to PDF."""
        return self._convert(input_file, output_file, "pdf")

    def pdf_to_docx(self, input_file: str, output_file: str) -> None:
        """Convert PDF to DOCX (requires LibreOffice)."""
        return self._convert(input_file, output_file, "docx")

    def pptx_to_pdf(self, input_file: str, output_file: str) -> None:
        """Convert PPTX to PDF."""
        return self._convert(input_file, output_file, "pdf")

    def xlsx_to_pdf(self, input_file: str, output_file: str) -> None:
        """Convert XLSX to PDF."""
        return self._convert(input_file, output_file, "pdf")

    # Helper functions
    @staticmethod
    def _is_libreoffice_installed() -> bool:
        """Check if LibreOffice is installed."""
        return which("libreoffice") or which("soffice")

    @staticmethod
    def _is_unoconv_installed() -> bool:
        """Check if LibreOffice is installed."""
        return which("unoconv")
