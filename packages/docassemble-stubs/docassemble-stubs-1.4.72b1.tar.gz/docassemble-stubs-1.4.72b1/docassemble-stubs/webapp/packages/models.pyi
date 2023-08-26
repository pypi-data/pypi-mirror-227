from _typeshed import Incomplete
from docassemble.base.config import dbtableprefix as dbtableprefix
from docassemble.webapp.db_object import db as db

class Package(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    name: Incomplete
    type: Incomplete
    giturl: Incomplete
    gitsubdir: Incomplete
    upload: Incomplete
    package_auth: Incomplete
    version: Incomplete
    packageversion: Incomplete
    limitation: Incomplete
    dependency: Incomplete
    core: Incomplete
    active: Incomplete
    gitbranch: Incomplete

class PackageAuth(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    package_id: Incomplete
    user_id: Incomplete
    authtype: Incomplete

class Install(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    hostname: Incomplete
    version: Incomplete
    packageversion: Incomplete
    package_id: Incomplete
