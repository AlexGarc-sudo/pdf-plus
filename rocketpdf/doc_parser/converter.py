from enum import IntEnum
from typing import Protocol
from click import secho


class FileConverter(Protocol):
    def docx_to_pdf(self, input_file: str, output_file: str): ...
    def pdf_to_docx(self, input_file: str, output_file: str): ...
    def pptx_to_pdf(self, input_file: str, output_file: str): ...
    def xlsx_to_pdf(self, input_file: str, output_file: str): ...


class FileFormat(IntEnum):
    # Word formats
    WORD_PDF = 17
    WORD_DOCX = 16

    # Excel formats
    EXCEL_PDF = 57
    EXCEL_XLSX = 51

    # PowerPoint formats
    PPT_PDF = 32
    PPT_PPTX = 1


class WindowsFileConverter:
    def __init__(self):
        import comtypes.client

        self._converter = comtypes.client.CreateObject

    def _conversion(
        self,
        input_file: str,
        output_file: str,
        app: str,
        attr: str,
        file_format: FileFormat,
    ):
        """
        Generic conversion function that works with different Microsoft Office applications.
        """
        try:
            application = self._converter(app)
            # document = application.__getattr__(attr).Open(input_file)
            attribute_obj = getattr(application, attr)
            document = attribute_obj.Open(input_file)
            document.SaveAs(output_file, FileFormat=file_format.value)
        except Exception as e:
            err_msg = f"\nError occurred: {e}\nException Type: {type(e).__name__}"
            secho(err_msg, fg="red")
        finally:
            document.Close()
            application.Quit()

    # Functions to convert different filetypes
    def docx_to_pdf(self, input_file: str, output_file: str):
        return self._conversion(
            input_file,
            output_file,
            "Word.Application",
            "Documents",
            FileFormat.WORD_PDF,
        )

    def pdf_to_docx(self, input_file: str, output_file: str):
        return self._conversion(
            input_file,
            output_file,
            "Word.Application",
            "Documents",
            FileFormat.WORD_DOCX,
        )

    def pptx_to_pdf(self, input_file: str, output_file: str):
        return self._conversion(
            input_file,
            output_file,
            "PowerPoint.Application",
            "Presentations",
            FileFormat.PPT_PDF,
        )

    def xlsx_to_pdf(self, input_file: str, output_file: str):
        return self._conversion(
            input_file,
            output_file,
            "Excel.Application",
            "Workbooks",
            FileFormat.EXCEL_PDF,
        )
