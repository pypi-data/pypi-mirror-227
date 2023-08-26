from _typeshed import Incomplete
from docassemble.base.error import DAException as DAException
from docassemble.base.generate_key import random_lower_string as random_lower_string
from docassemble.base.logger import logmessage as logmessage
from docassemble.webapp.core.models import Uploads as Uploads, UploadsRoleAuth as UploadsRoleAuth, UploadsUserAuth as UploadsUserAuth
from docassemble.webapp.db_object import db as db
from docassemble.webapp.files import SavedFile as SavedFile, get_ext_and_mimetype as get_ext_and_mimetype
from docassemble.webapp.users.models import UserDictKeys as UserDictKeys, UserRoles as UserRoles

cloud: Incomplete
QPDF_PATH: str

def url_if_exists(file_reference, **kwargs): ...
def get_version_parameter(package): ...
def get_info_from_file_reference(file_reference, **kwargs): ...
def add_info_about_file(filename, basename, result) -> None: ...
def get_info_from_file_number(file_number, privileged: bool = ..., filename: Incomplete | None = ..., uids: Incomplete | None = ...): ...
