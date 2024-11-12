# import fitz

from .clitools import spinner
from .converter import LOCAL_ENGINE, ConverterEngine


@spinner("Converting docx to pdf file")
def docx_to_pdf(in_file: str, out_file: str, converter: ConverterEngine = LOCAL_ENGINE) -> None:
    return converter.docx_to_pdf(in_file, out_file)


@spinner("Converting pdf to docx file")
def pdf_to_docx(in_file: str, out_file: str, converter: ConverterEngine = LOCAL_ENGINE) -> None:
    return converter.pdf_to_docx(in_file, out_file)


@spinner("Converting pdf to pptx file")
def pptx_to_pdf(in_file: str, out_file: str, converter: ConverterEngine = LOCAL_ENGINE) -> None:
    return converter.pptx_to_pdf(in_file, out_file)


@spinner("Converting pdf to xlsx file")
def xlsx_to_pdf(in_file: str, out_file: str, converter: ConverterEngine = LOCAL_ENGINE) -> None:
    return converter.xlsx_to_pdf(in_file, out_file)
