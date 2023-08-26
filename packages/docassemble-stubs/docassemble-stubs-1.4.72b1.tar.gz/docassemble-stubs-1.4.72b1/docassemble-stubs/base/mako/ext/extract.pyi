from _typeshed import Incomplete
from collections.abc import Generator
from docassemble.base.mako import lexer as lexer, parsetree as parsetree

class MessageExtractor:
    use_bytes: bool
    def process_file(self, fileobj) -> None: ...
    def extract_nodes(self, nodes) -> Generator[Incomplete, None, None]: ...
    @staticmethod
    def _split_comment(lineno, comment): ...
