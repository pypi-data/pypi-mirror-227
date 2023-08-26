from _typeshed import Incomplete
from docassemble.base.config import daconfig as daconfig
from docassemble.base.error import DAError as DAError
from docassemble.base.logger import logmessage as logmessage
from docassemble.base.pdfa import pdf_to_pdfa as pdf_to_pdfa
from docassemble.base.pdftk import pdf_encrypt as pdf_encrypt

style_find: Incomplete
PANDOC_PATH: Incomplete

def copy_if_different(source, destination) -> None: ...
def cloudconvert_to_pdf(in_format, from_file, to_file, pdfa, password) -> None: ...
def convertapi_to_pdf(from_file, to_file) -> None: ...
def get_pandoc_version(): ...

PANDOC_INITIALIZED: bool
PANDOC_OLD: bool
PANDOC_ENGINE: Incomplete

def initialize_pandoc() -> None: ...

UNOCONV_PATH: Incomplete
UNOCONV_AVAILABLE: Incomplete
UNOCONV_FILTERS: Incomplete
LIBREOFFICE_PATH: Incomplete
LIBREOFFICE_MACRO_PATH: Incomplete
LIBREOFFICE_INITIALIZED: bool
convertible_mimetypes: Incomplete
convertible_extensions: Incomplete

class MyPandoc:
    pdfa: bool
    password: Incomplete
    input_content: Incomplete
    output_content: Incomplete
    input_format: str
    output_format: str
    output_extension: str
    output_filename: Incomplete
    template_file: Incomplete
    reference_file: Incomplete
    metadata: Incomplete
    initial_yaml: Incomplete
    additional_yaml: Incomplete
    arguments: Incomplete
    def __init__(self, **kwargs) -> None: ...
    pandoc_message: Incomplete
    def convert_to_file(self, question) -> None: ...
    def convert(self, question) -> None: ...

def word_to_pdf(in_file, in_format, out_file, pdfa: bool = ..., password: Incomplete | None = ..., update_refs: bool = ..., tagged: bool = ..., filename: Incomplete | None = ..., retry: bool = ...): ...
def rtf_to_docx(in_file, out_file): ...
def convert_file(in_file, out_file, input_extension, output_extension): ...
def word_to_markdown(in_file, in_format): ...
def get_rtf_styles(filename): ...
def update_references(filename): ...
def initialize_libreoffice() -> None: ...
def concatenate_files(path_list, pdfa: bool = ..., password: Incomplete | None = ...): ...
