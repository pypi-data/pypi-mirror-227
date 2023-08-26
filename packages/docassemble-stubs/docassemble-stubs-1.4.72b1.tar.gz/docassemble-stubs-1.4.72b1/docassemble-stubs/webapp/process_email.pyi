from _typeshed import Incomplete
from docassemble.webapp.core.models import Email as Email, EmailAttachment as EmailAttachment, Shortener as Shortener
from docassemble.webapp.file_number import get_new_file_number as get_new_file_number
from docassemble.webapp.files import SavedFile as SavedFile
from docassemble.webapp.users.models import UserModel as UserModel

db: Incomplete

def main() -> None: ...
def save_attachment(uid, yaml_filename, filename, email_id, index, content_type, extension, content) -> None: ...
def secure_filename(filename): ...
