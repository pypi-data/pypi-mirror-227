from _typeshed import Incomplete
from celery import Celery # type: ignore
from collections.abc import Generator
from docassemble.base.config import daconfig as daconfig
from docassemble.base.logger import logmessage as logmessage

backend: Incomplete
broker: Incomplete
workerapp: Incomplete

class WorkerController:
    loaded: bool
    def __init__(self) -> None: ...
    flaskapp: Incomplete
    set_request_active: Incomplete
    fetch_user_dict: Incomplete
    save_user_dict: Incomplete
    obtain_lock: Incomplete
    obtain_lock_patiently: Incomplete
    release_lock: Incomplete
    Message: Incomplete
    reset_user_dict: Incomplete
    da_send_mail: Incomplete
    functions: Incomplete
    interview_cache: Incomplete
    parse: Incomplete
    retrieve_email: Incomplete
    get_info_from_file_number: Incomplete
    trigger_update: Incomplete
    util: Incomplete
    r: Incomplete
    apiclient: Incomplete
    get_ext_and_mimetype: Incomplete
    get_user_object: Incomplete
    login_user: Incomplete
    update_last_login: Incomplete
    error_notification: Incomplete
    noquote: Incomplete
    update: Incomplete
    def initialize(self) -> None: ...

worker_controller: Incomplete

def convert(obj): ...
def process_error(interview, session_code, yaml_filename, secret, user_info, url, url_root, is_encrypted, error_type, error_message, error_trace, variables, extra): ...
def error_object(err): ...
def bg_context() -> Generator[Incomplete, None, None]: ...
