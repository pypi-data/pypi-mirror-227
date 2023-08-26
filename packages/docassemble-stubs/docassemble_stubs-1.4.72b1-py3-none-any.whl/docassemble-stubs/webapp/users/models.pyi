from _typeshed import Incomplete
from docassemble.base.config import allowed as allowed, dbtableprefix as dbtableprefix
from docassemble.webapp.db_object import UserMixin as UserMixin, db as db
from flask_login import AnonymousUserMixin # type: ignore

class AnonymousUserModel(AnonymousUserMixin):
    @property
    def id(self): ...
    def same_as(self, user_id): ...
    def has_role(self, *pargs, **kwargs): ...
    def has_roles(self, *pargs, **kwargs): ...
    def has_role_or_permission(self, *specified_role_names, permissions: Incomplete | None = ...): ...
    def can_do(self, task): ...

class UserModel(db.Model, UserMixin):
    __tablename__: Incomplete
    id: Incomplete
    social_id: Incomplete
    nickname: Incomplete
    email: Incomplete
    confirmed_at: Incomplete
    active: Incomplete
    first_name: Incomplete
    last_name: Incomplete
    country: Incomplete
    subdivisionfirst: Incomplete
    subdivisionsecond: Incomplete
    subdivisionthird: Incomplete
    organization: Incomplete
    timezone: Incomplete
    language: Incomplete
    user_auth: Incomplete
    roles: Incomplete
    password: Incomplete
    otp_secret: Incomplete
    pypi_username: Incomplete
    pypi_password: Incomplete
    modified_at: Incomplete
    last_login: Incomplete
    limited_api: bool
    def same_as(self, user_id): ...
    def has_role(self, *specified_role_names): ...
    def has_role_or_permission(self, *specified_role_names, permissions: Incomplete | None = ...): ...
    def can_do(self, task): ...

class UserAuthModel(db.Model, UserMixin):
    __tablename__: Incomplete
    id: Incomplete
    user_id: Incomplete
    password: Incomplete
    reset_password_token: Incomplete
    user: Incomplete

class Role(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    name: Incomplete
    description: Incomplete

class UserRoles(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    user_id: Incomplete
    role_id: Incomplete

class UserDict(db.Model):
    __tablename__: Incomplete
    indexno: Incomplete
    filename: Incomplete
    key: Incomplete
    dictionary: Incomplete
    user_id: Incomplete
    encrypted: Incomplete
    modtime: Incomplete

class UserDictKeys(db.Model):
    __tablename__: Incomplete
    indexno: Incomplete
    filename: Incomplete
    key: Incomplete
    user_id: Incomplete
    temp_user_id: Incomplete

class TempUser(db.Model):
    __tablename__: Incomplete
    id: Incomplete

class ChatLog(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    filename: Incomplete
    key: Incomplete
    message: Incomplete
    user_id: Incomplete
    temp_user_id: Incomplete
    owner_id: Incomplete
    temp_owner_id: Incomplete
    open_to_peer: Incomplete
    encrypted: Incomplete
    modtime: Incomplete

class MyUserInvitation(db.Model):
    __tablename__: Incomplete
    id: Incomplete
    email: Incomplete
    role_id: Incomplete
    invited_by_user_id: Incomplete
    token: Incomplete
