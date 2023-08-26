from _typeshed import Incomplete
from docassemble.base.config import dbtableprefix as dbtableprefix
from docassemble.webapp.database import dbprefix as dbprefix
from docassemble.webapp.db_object import db as db

class Uploads(db.Model):
    __tablename__: Incomplete
    indexno: Incomplete
    key: Incomplete
    filename: Incomplete
    yamlfile: Incomplete
    private: Incomplete
    persistent: Incomplete

class UploadsUserAuth(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    uploads_indexno: Incomplete
    user_id: Incomplete
    temp_user_id: Incomplete

class UploadsRoleAuth(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    uploads_indexno: Incomplete
    role_id: Incomplete

class ObjectStorage(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    key: Incomplete
    value: Incomplete

class SpeakList(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    filename: Incomplete
    key: Incomplete
    phrase: Incomplete
    question: Incomplete
    type: Incomplete
    language: Incomplete
    dialect: Incomplete
    voice: Incomplete
    upload: Incomplete
    encrypted: Incomplete
    digest: Incomplete

class Supervisors(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    hostname: Incomplete
    url: Incomplete
    start_time: Incomplete
    role: Incomplete

class MachineLearning(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    group_id: Incomplete
    key: Incomplete
    independent: Incomplete
    dependent: Incomplete
    info: Incomplete
    create_time: Incomplete
    modtime: Incomplete
    active: Incomplete

class Shortener(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    short: Incomplete
    filename: Incomplete
    uid: Incomplete
    user_id: Incomplete
    temp_user_id: Incomplete
    key: Incomplete
    index: Incomplete
    modtime: Incomplete

class Email(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    short: Incomplete
    all_addr: Incomplete
    to_addr: Incomplete
    cc_addr: Incomplete
    from_addr: Incomplete
    reply_to_addr: Incomplete
    return_path_addr: Incomplete
    subject: Incomplete
    datetime_message: Incomplete
    datetime_received: Incomplete

class EmailAttachment(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    email_id: Incomplete
    index: Incomplete
    content_type: Incomplete
    extension: Incomplete
    upload: Incomplete

class GlobalObjectStorage(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    key: Incomplete
    value: Incomplete
    encrypted: Incomplete
    user_id: Incomplete
    temp_user_id: Incomplete

class JsonStorage(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    filename: Incomplete
    key: Incomplete
    data: Incomplete
    tags: Incomplete
    modtime: Incomplete
    persistent: Incomplete
