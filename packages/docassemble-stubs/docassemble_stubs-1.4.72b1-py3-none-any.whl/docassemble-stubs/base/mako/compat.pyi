from _typeshed import Incomplete
from typing import NamedTuple

win32: Incomplete
pypy: Incomplete
py38: Incomplete

class ArgSpec(NamedTuple):
    args: Incomplete
    varargs: Incomplete
    keywords: Incomplete
    defaults: Incomplete

def inspect_getargspec(func): ...
def load_module(module_id, path): ...
def exception_as(): ...
def exception_name(exc): ...
def importlib_metadata_get(group): ...
