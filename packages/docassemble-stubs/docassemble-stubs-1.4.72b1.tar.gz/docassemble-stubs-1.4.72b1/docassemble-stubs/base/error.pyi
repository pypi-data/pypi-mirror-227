from _typeshed import Incomplete
from re import Pattern

valid_variable_match: Pattern
match_brackets_or_dot: Pattern

class DAIndexError(IndexError): ...
class DAAttributeError(AttributeError): ...

class DAException(Exception): ...

class DAError(Exception):
    value: Incomplete
    error_code: Incomplete
    def __init__(self, value, code: int = ...) -> None: ...
    def __str__(self): ...

class DANotFoundError(Exception): ...

class DAValidationError(Exception):
    field: Incomplete
    def __init__(self, *pargs, field: Incomplete | None = ...) -> None: ...

class CodeExecute(Exception):
    compute: Incomplete
    question: Incomplete
    def __init__(self, compute, question) -> None: ...

class ForcedReRun(Exception): ...
class LazyNameError(NameError): ...
class DANameError(NameError): ...

def invalid_variable_name(varname) -> bool: ...
def intrinsic_name_of(var_name, the_user_dict)-> str: ...

class ForcedNameError(NameError):
    next_action: Incomplete
    arguments: Incomplete
    def __init__(self, *pargs, **kwargs) -> None: ...
    name: Incomplete
    context: Incomplete
    def set_action(self, data) -> None: ...

class DAErrorNoEndpoint(DAError): ...

class DAErrorMissingVariable(DAError):
    value: Incomplete
    variable: Incomplete
    error_code: Incomplete
    def __init__(self, value, variable: Incomplete | None = ..., code: int = ...) -> None: ...

class DAErrorCompileError(DAError): ...

class MandatoryQuestion(Exception):
    value: str
    def __init__(self) -> None: ...
    def __str__(self): ...

class QuestionError(Exception):
    question: Incomplete
    subquestion: Incomplete
    url: Incomplete
    show_leave: Incomplete
    show_exit: Incomplete
    reload: Incomplete
    show_restart: Incomplete
    buttons: Incomplete
    dead_end: Incomplete
    def __init__(self, *pargs, **kwargs) -> None: ...
    def __str__(self): ...

class BackgroundResponseError(Exception):
    backgroundresponse: Incomplete
    sleep: Incomplete
    def __init__(self, *pargs, **kwargs) -> None: ...
    def __str__(self): ...

class BackgroundResponseActionError(Exception):
    action: Incomplete
    def __init__(self, *pargs, **kwargs) -> None: ...
    def __str__(self): ...

class ResponseError(Exception):
    response: str
    binaryresponse: Incomplete
    filename: Incomplete
    url: Incomplete
    nullresponse: Incomplete
    response_code: Incomplete
    sleep: Incomplete
    all_variables: Incomplete
    include_internal: Incomplete
    content_type: Incomplete
    def __init__(self, *pargs, **kwargs) -> None: ...
    def __str__(self): ...

class CommandError(Exception):
    return_type: Incomplete
    url: Incomplete
    sleep: Incomplete
    def __init__(self, *pargs, **kwargs) -> None: ...
    def __str__(self): ...

class DAWebError(Exception):
    def __init__(self, **kwargs) -> None: ...
