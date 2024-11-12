# TODO: IMPLEMENT AND TEST MACOS CONVERTER


class DarwinConverterEngine:
    def __init__(self):
        raise NotImplementedError()

    def docx_to_pdf(self, input_file: str, output_file: str) -> None: ...

    def pdf_to_docx(self, input_file: str, output_file: str) -> None: ...

    def pptx_to_pdf(self, input_file: str, output_file: str) -> None: ...

    def xlsx_to_pdf(self, input_file: str, output_file: str) -> None: ...
