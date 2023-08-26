from _typeshed import Incomplete
from typing import Tuple
from flask import Flask
from flask_socketio import SocketIO # type: ignore
from sqlalchemy import Engine

def create_app() -> Tuple[Flask, Engine, SocketIO]: ...

app: Incomplete
db: Incomplete
socketio: Incomplete
