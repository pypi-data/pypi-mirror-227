from _typeshed import Incomplete
from docassemble.webapp.app_socket import app as app
from flask import Flask
from flask_wtf.csrf import CSRFProtect # type: ignore
from typing import Tuple

proxyfix_version: int

def create_app() -> Tuple[Flask, CSRFProtect]: ...

csrf: CSRFProtect
