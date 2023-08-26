from _typeshed import Incomplete
from docassemble.base.config import daconfig as daconfig
from docassemble.base.functions import server as server
from docassemble.webapp.core.models import JsonStorage as CoreJsonStorage

custom_db: Incomplete
JsonDb: Incomplete
JsonStorage = Incomplete

def variables_snapshot_connection(): ...

Base: Incomplete
url: Incomplete

connect_args: Incomplete
engine: Incomplete

def read_answer_json(user_code, filename, tags: Incomplete | None = ..., all_tags: bool = ...): ...
def write_answer_json(user_code, filename, data, tags: Incomplete | None = ..., persistent: bool = ...) -> None: ...
def delete_answer_json(user_code, filename, tags: Incomplete | None = ..., delete_all: bool = ..., delete_persistent: bool = ...) -> None: ...
