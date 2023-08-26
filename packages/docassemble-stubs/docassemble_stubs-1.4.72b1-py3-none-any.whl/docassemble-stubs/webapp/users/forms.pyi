from _typeshed import Incomplete
from docassemble.base.config import daconfig as daconfig
from docassemble.base.functions import LazyArray as LazyArray
from docassemble.base.generate_key import random_alphanumeric as random_alphanumeric
from docassemble.base.logger import logmessage as logmessage
from docassemble.webapp.daredis import r as r
from docassemble.webapp.db_object import db as db
from docassemble.webapp.users.models import Role as Role, UserModel as UserModel
from docassemble_flask_user.forms import LoginForm, RegisterForm # type: ignore
from flask_wtf import FlaskForm # type: ignore

HTTP_TO_HTTPS: Incomplete
BAN_IP_ADDRESSES: Incomplete

def get_requester_ip(req): ...
def fix_nickname(form, field) -> None: ...

class MySignInForm(LoginForm):
    def validate(self): ...

def da_unique_email_validator(form, field): ...
def da_registration_restrict_validator(form, field): ...

class MyRegisterForm(RegisterForm):
    first_name: Incomplete
    last_name: Incomplete
    country: Incomplete
    subdivisionfirst: Incomplete
    subdivisionsecond: Incomplete
    subdivisionthird: Incomplete
    organization: Incomplete
    language: Incomplete
    timezone: Incomplete
    nickname: Incomplete
    email: Incomplete

def length_two(form, field) -> None: ...

class NewPrivilegeForm(FlaskForm):
    name: Incomplete
    submit: Incomplete

class UserProfileForm(FlaskForm):
    first_name: Incomplete
    last_name: Incomplete
    country: Incomplete
    subdivisionfirst: Incomplete
    subdivisionsecond: Incomplete
    subdivisionthird: Incomplete
    organization: Incomplete
    language: Incomplete
    timezone: Incomplete
    pypi_username: Incomplete
    pypi_password: Incomplete
    confirmed_at: Incomplete
    submit: Incomplete
    cancel: Incomplete

class EditUserProfileForm(UserProfileForm):
    email: Incomplete
    role_id: Incomplete
    active: Incomplete
    uses_mfa: Incomplete
    def validate(self, user_id, admin_id): ...

class PhoneUserProfileForm(UserProfileForm):
    def validate(self): ...
    email: Incomplete

class RequestDeveloperForm(FlaskForm):
    reason: Incomplete
    submit: Incomplete

class MyInviteForm(FlaskForm):
    def validate(self): ...
    email: Incomplete
    role_id: Incomplete
    next: Incomplete
    submit: Incomplete

class UserAddForm(FlaskForm):
    email: Incomplete
    first_name: Incomplete
    last_name: Incomplete
    role_id: Incomplete
    password: Incomplete
    submit: Incomplete

class PhoneLoginForm(FlaskForm):
    phone_number: Incomplete
    submit: Incomplete

class PhoneLoginVerifyForm(FlaskForm):
    phone_number: Incomplete
    verification_code: Incomplete
    submit: Incomplete
    def validate(self): ...

class MFASetupForm(FlaskForm):
    verification_code: Incomplete
    submit: Incomplete

class MFALoginForm(FlaskForm):
    verification_code: Incomplete
    next: Incomplete
    submit: Incomplete

class MFAReconfigureForm(FlaskForm):
    reconfigure: Incomplete
    disable: Incomplete
    cancel: Incomplete

class MFAChooseForm(FlaskForm):
    auth: Incomplete
    sms: Incomplete
    cancel: Incomplete

class MFASMSSetupForm(FlaskForm):
    phone_number: Incomplete
    submit: Incomplete

class MFAVerifySMSSetupForm(FlaskForm):
    verification_code: Incomplete
    submit: Incomplete

class MyResendConfirmEmailForm(FlaskForm):
    email: Incomplete
    submit: Incomplete

class ManageAccountForm(FlaskForm):
    confirm: Incomplete
    delete: Incomplete

class InterviewsListForm(FlaskForm):
    i: Incomplete
    session: Incomplete
    tags: Incomplete
    delete: Incomplete
    delete_all: Incomplete
