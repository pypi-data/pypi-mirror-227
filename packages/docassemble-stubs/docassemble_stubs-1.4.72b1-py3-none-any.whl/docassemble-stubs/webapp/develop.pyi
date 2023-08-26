from _typeshed import Incomplete
from flask_wtf import FlaskForm # type: ignore
from wtforms import SelectField # type: ignore

class NonValidatingSelectField(SelectField):
    def pre_validate(self, form) -> None: ...

def validate_project_name(form, field) -> None: ...
def validate_name(form, field) -> None: ...
def validate_package_version(form, field) -> None: ...
def validate_package_name(form, field) -> None: ...

class CreatePackageForm(FlaskForm):
    name: Incomplete
    submit: Incomplete

class CreatePlaygroundPackageForm(FlaskForm):
    name: Incomplete
    submit: Incomplete

class UpdatePackageForm(FlaskForm):
    giturl: Incomplete
    gitbranch: Incomplete
    zipfile: Incomplete
    pippackage: Incomplete
    submit: Incomplete

class ConfigForm(FlaskForm):
    config_content: Incomplete
    submit: Incomplete
    cancel: Incomplete

class PlaygroundForm(FlaskForm):
    status: Incomplete
    original_playground_name: Incomplete
    playground_name: Incomplete
    playground_content: Incomplete
    search_term: Incomplete
    submit: Incomplete
    run: Incomplete
    delete: Incomplete

class PlaygroundUploadForm(FlaskForm):
    uploadfile: Incomplete

class LogForm(FlaskForm):
    filter_string: Incomplete
    file_name: Incomplete
    submit: Incomplete
    clear: Incomplete

class Utilities(FlaskForm):
    pdfdocxfile: Incomplete
    scan: Incomplete
    interview: Incomplete
    interview_submit: Incomplete
    language: Incomplete
    tr_language: Incomplete
    systemfiletype: Incomplete
    filetype: Incomplete
    language_submit: Incomplete
    officeaddin_version: Incomplete
    officeaddin_submit: Incomplete

class PlaygroundFilesForm(FlaskForm):
    purpose: Incomplete
    section: Incomplete
    uploadfile: Incomplete
    submit: Incomplete

class PlaygroundFilesEditForm(FlaskForm):
    purpose: Incomplete
    section: Incomplete
    original_file_name: Incomplete
    file_name: Incomplete
    search_term: Incomplete
    file_content: Incomplete
    active_file: Incomplete
    submit: Incomplete
    delete: Incomplete

class RenameProject(FlaskForm):
    name: Incomplete
    submit: Incomplete

class DeleteProject(FlaskForm):
    submit: Incomplete

class NewProject(FlaskForm):
    name: Incomplete
    submit: Incomplete

class PullPlaygroundPackage(FlaskForm):
    github_url: Incomplete
    github_branch: Incomplete
    pypi: Incomplete
    pull: Incomplete
    cancel: Incomplete

class PlaygroundPackagesForm(FlaskForm):
    original_file_name: Incomplete
    file_name: Incomplete
    license: Incomplete
    author_name: Incomplete
    author_email: Incomplete
    description: Incomplete
    version: Incomplete
    url: Incomplete
    dependencies: Incomplete
    interview_files: Incomplete
    template_files: Incomplete
    module_files: Incomplete
    static_files: Incomplete
    sources_files: Incomplete
    readme: Incomplete
    github_branch: Incomplete
    github_branch_new: Incomplete
    commit_message: Incomplete
    pypi_also: Incomplete
    install_also: Incomplete
    submit: Incomplete
    download: Incomplete
    install: Incomplete
    pypi: Incomplete
    github: Incomplete
    cancel: Incomplete
    delete: Incomplete

class GoogleDriveForm(FlaskForm):
    folder: Incomplete
    submit: Incomplete
    cancel: Incomplete

class OneDriveForm(FlaskForm):
    folder: Incomplete
    submit: Incomplete
    cancel: Incomplete

class GitHubForm(FlaskForm):
    shared: Incomplete
    orgs: Incomplete
    save: Incomplete
    configure: Incomplete
    unconfigure: Incomplete
    cancel: Incomplete

class TrainingForm(FlaskForm):
    the_package: Incomplete
    the_file: Incomplete
    the_group_id: Incomplete
    show_all: Incomplete
    submit: Incomplete
    cancel: Incomplete

class TrainingUploadForm(FlaskForm):
    usepackage: Incomplete
    jsonfile: Incomplete
    importtype: Incomplete
    submit: Incomplete

class AddinUploadForm(FlaskForm):
    content: Incomplete
    filename: Incomplete

class FunctionFileForm(FlaskForm): ...

class APIKey(FlaskForm):
    action: Incomplete
    key: Incomplete
    security: Incomplete
    name: Incomplete
    method: Incomplete
    permissions: Incomplete
    submit: Incomplete
    delete: Incomplete
    def validate(self, extra_validators: Incomplete | None = ...): ...
