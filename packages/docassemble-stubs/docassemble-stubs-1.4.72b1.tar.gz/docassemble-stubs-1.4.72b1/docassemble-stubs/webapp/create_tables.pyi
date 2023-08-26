from _typeshed import Incomplete
from docassemble.base.config import daconfig as daconfig
from docassemble.base.functions import word as word
from docassemble.base.generate_key import random_alphanumeric as random_alphanumeric
from docassemble.base.logger import logmessage as logmessage
from docassemble.webapp.api_key import add_specific_api_key as add_specific_api_key
from docassemble.webapp.app_object import app as app
from docassemble.webapp.core.models import GlobalObjectStorage as GlobalObjectStorage, MachineLearning as MachineLearning, ObjectStorage as ObjectStorage, Shortener as Shortener, SpeakList as SpeakList, Uploads as Uploads # type: ignore
from docassemble.webapp.database import alchemy_connection_string as alchemy_connection_string, dbprefix as dbprefix, dbtableprefix as dbtableprefix
from docassemble.webapp.db_object import db as db
from docassemble.webapp.packages.models import Package as Package
from docassemble.webapp.update import add_dependencies as add_dependencies
from docassemble.webapp.users.models import ChatLog as ChatLog, MyUserInvitation as MyUserInvitation, Role as Role, TempUser as TempUser, UserAuthModel as UserAuthModel, UserDict as UserDict, UserDictKeys as UserDictKeys, UserModel as UserModel, UserRoles as UserRoles # type: ignore
from pathlib import Path as Path

def get_role(the_db, name, result: Incomplete | None = ...): ...
def get_user(the_db, role, defaults, result: Incomplete | None = ...): ...
def test_for_errors(start_time: Incomplete | None = ...) -> None: ...
def populate_tables(start_time: Incomplete | None = ...) -> None: ...
def main() -> None: ...
