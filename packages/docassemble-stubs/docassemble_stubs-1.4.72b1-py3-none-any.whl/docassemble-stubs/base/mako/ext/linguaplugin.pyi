from _typeshed import Incomplete
from collections.abc import Generator
from docassemble.base.mako.ext.extract import MessageExtractor as MessageExtractor
from lingua.extractors import Extractor # type: ignore

class LinguaMakoExtractor(Extractor, MessageExtractor):
    use_bytes: bool
    extensions: Incomplete
    default_config: Incomplete
    options: Incomplete
    filename: Incomplete
    python_extractor: Incomplete
    def __call__(self, filename, options, fileobj: Incomplete | None = ...) -> None: ...
    def process_python(self, code, code_lineno, translator_strings) -> Generator[Incomplete, None, None]: ...
