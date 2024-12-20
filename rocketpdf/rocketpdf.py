import fitz

from .clitools import spinner
from .converter import LOCAL_ENGINE, ConverterEngine


@spinner("Converting docx to pdf file")
def docx_to_pdf(in_file: str, out_file: str, converter: ConverterEngine = LOCAL_ENGINE()) -> None:
    return converter.docx_to_pdf(in_file, out_file)


@spinner("Converting pdf to docx file")
def pdf_to_docx(in_file: str, out_file: str, converter: ConverterEngine = LOCAL_ENGINE()) -> None:
    return converter.pdf_to_docx(in_file, out_file)


@spinner("Converting pdf to pptx file")
def pptx_to_pdf(in_file: str, out_file: str, converter: ConverterEngine = LOCAL_ENGINE()) -> None:
    return converter.pptx_to_pdf(in_file, out_file)


@spinner("Converting pdf to xlsx file")
def xlsx_to_pdf(in_file: str, out_file: str, converter: ConverterEngine = LOCAL_ENGINE()) -> None:
    return converter.xlsx_to_pdf(in_file, out_file)


@spinner("Extracting pages")
def extract_pages(
    in_file: str, start: int, end: int, out_file: str = None, compress: bool = False
) -> None:
    with fitz.open(in_file) as file_to_extract:
        if start < 1 or end > len(file_to_extract) or start > end:
            raise ValueError("Invalid page range specified.")

        with fitz.open() as new_file:
            new_file.insert_pdf(file_to_extract, from_page=start - 1, to_page=end - 1)
            new_filename = out_file or f"{in_file} {start}-{end}"
            return new_file.save(new_filename, deflate=compress)


# @spinner("Merging PDFs")
# def merge_pdf():
#     with open


@spinner("Compressing PDF")
def compress_pdf(in_file: str, out_file: str = None, compress_image: bool = True) -> None:
    filename = out_file or f"{in_file}-compressed"

    with fitz.open(in_file) as file_to_compress:
        with fitz.open() as new_file:
            new_file.insert_pdf(file_to_compress)
            return new_file.save(filename, garbage=3, deflate=True, deflate_images=compress_image)
