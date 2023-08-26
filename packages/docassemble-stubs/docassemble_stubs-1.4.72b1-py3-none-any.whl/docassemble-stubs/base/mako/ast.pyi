from _typeshed import Incomplete
from docassemble.base.astparser import myvisitnode as myvisitnode
from docassemble.base.mako import exceptions as exceptions, pyparser as pyparser

class PythonCode:
    names_used: Incomplete
    names_set: Incomplete
    code: Incomplete
    declared_identifiers: Incomplete
    undeclared_identifiers: Incomplete
    def __init__(self, code, **exception_kwargs) -> None: ...

class ArgumentList:
    codeargs: Incomplete
    args: Incomplete
    declared_identifiers: Incomplete
    undeclared_identifiers: Incomplete
    def __init__(self, code, **exception_kwargs) -> None: ...

class PythonFragment(PythonCode):
    names_set: Incomplete
    def __init__(self, code, **exception_kwargs) -> None: ...

class FunctionDecl:
    code: Incomplete
    def __init__(self, code, allow_kwargs: bool = ..., **exception_kwargs) -> None: ...
    def get_argument_expressions(self, as_call: bool = ...): ...
    @property
    def allargnames(self): ...

class FunctionArgs(FunctionDecl):
    def __init__(self, code, **kwargs) -> None: ...
