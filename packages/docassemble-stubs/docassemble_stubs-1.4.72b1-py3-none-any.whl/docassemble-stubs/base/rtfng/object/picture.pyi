from _typeshed import Incomplete
from docassemble.base.rtfng.document.base import RawCode as RawCode

def _get_jpg_dimensions(fin): ...

_PNG_HEADER: bytes

def _get_png_dimensions(data): ...

class Image(RawCode):
    PNG_LIB: str
    JPG_LIB: str
    PICT_TYPES: Incomplete
    def __init__(self, file_name, **kwargs) -> None: ...
    def ToRawCode(self, var_name): ...
