from _typeshed import Incomplete
from docassemble.base.mako import cache as cache, codegen as codegen, compat as compat, exceptions as exceptions, runtime as runtime, util as util
from docassemble.base.mako.lexer import Lexer as Lexer

class Template:
    lexer_cls: Incomplete
    names_used: Incomplete
    names_set: Incomplete
    module_id: Incomplete
    uri: Incomplete
    input_encoding: Incomplete
    output_encoding: Incomplete
    encoding_errors: Incomplete
    enable_loop: Incomplete
    strict_undefined: Incomplete
    module_writer: Incomplete
    default_filters: Incomplete
    buffer_filters: Incomplete
    imports: Incomplete
    future_imports: Incomplete
    preprocessor: Incomplete
    _code: Incomplete
    _source: Incomplete
    module: Incomplete
    filename: Incomplete
    callable_: Incomplete
    format_exceptions: Incomplete
    error_handler: Incomplete
    include_error_handler: Incomplete
    lookup: Incomplete
    module_directory: Incomplete
    def __init__(self, text: Incomplete | None = ..., filename: Incomplete | None = ..., uri: Incomplete | None = ..., format_exceptions: bool = ..., error_handler: Incomplete | None = ..., lookup: Incomplete | None = ..., output_encoding: Incomplete | None = ..., encoding_errors: str = ..., module_directory: Incomplete | None = ..., cache_args: Incomplete | None = ..., cache_impl: str = ..., cache_enabled: bool = ..., cache_type: Incomplete | None = ..., cache_dir: Incomplete | None = ..., cache_url: Incomplete | None = ..., module_filename: Incomplete | None = ..., input_encoding: Incomplete | None = ..., module_writer: Incomplete | None = ..., default_filters: Incomplete | None = ..., buffer_filters=..., strict_undefined: bool = ..., imports: Incomplete | None = ..., future_imports: Incomplete | None = ..., enable_loop: bool = ..., preprocessor: Incomplete | None = ..., lexer_cls: Incomplete | None = ..., include_error_handler: Incomplete | None = ...) -> None: ...
    @util.memoized_property
    def reserved_names(self): ...
    cache_impl: Incomplete
    cache_enabled: Incomplete
    cache_args: Incomplete
    def _setup_cache_args(self, cache_impl, cache_enabled, cache_args, cache_type, cache_dir, cache_url) -> None: ...
    def _compile_from_file(self, path, filename): ...
    @property
    def source(self): ...
    @property
    def code(self): ...
    @util.memoized_property
    def cache(self): ...
    @property
    def cache_dir(self): ...
    @property
    def cache_url(self): ...
    @property
    def cache_type(self): ...
    def render(self, *args, **data): ...
    def render_unicode(self, *args, **data): ...
    def render_context(self, context, *args, **kwargs) -> None: ...
    def has_def(self, name): ...
    def get_def(self, name): ...
    def list_defs(self): ...
    def _get_def_callable(self, name): ...
    @property
    def last_modified(self): ...

class ModuleTemplate(Template):
    module_id: Incomplete
    uri: Incomplete
    input_encoding: Incomplete
    output_encoding: Incomplete
    encoding_errors: Incomplete
    enable_loop: Incomplete
    module: Incomplete
    filename: Incomplete
    callable_: Incomplete
    format_exceptions: Incomplete
    error_handler: Incomplete
    include_error_handler: Incomplete
    lookup: Incomplete
    def __init__(self, module, module_filename: Incomplete | None = ..., template: Incomplete | None = ..., template_filename: Incomplete | None = ..., module_source: Incomplete | None = ..., template_source: Incomplete | None = ..., output_encoding: Incomplete | None = ..., encoding_errors: str = ..., format_exceptions: bool = ..., error_handler: Incomplete | None = ..., lookup: Incomplete | None = ..., cache_args: Incomplete | None = ..., cache_impl: str = ..., cache_enabled: bool = ..., cache_type: Incomplete | None = ..., cache_dir: Incomplete | None = ..., cache_url: Incomplete | None = ..., include_error_handler: Incomplete | None = ...) -> None: ...

class DefTemplate(Template):
    parent: Incomplete
    callable_: Incomplete
    output_encoding: Incomplete
    module: Incomplete
    encoding_errors: Incomplete
    format_exceptions: Incomplete
    error_handler: Incomplete
    include_error_handler: Incomplete
    enable_loop: Incomplete
    lookup: Incomplete
    def __init__(self, parent, callable_) -> None: ...
    def get_def(self, name): ...

class ModuleInfo:
    _modules: Incomplete
    module: Incomplete
    module_filename: Incomplete
    template_filename: Incomplete
    module_source: Incomplete
    template_source: Incomplete
    template_uri: Incomplete
    def __init__(self, module, module_filename, template, template_filename, module_source, template_source, template_uri) -> None: ...
    @classmethod
    def get_module_source_metadata(cls, module_source, full_line_map: bool = ...): ...
    @property
    def code(self): ...
    @property
    def source(self): ...

def _compile(template, text, filename, generate_magic_comment): ...
def _compile_text(template, text, filename): ...
def _compile_module_file(template, text, filename, outputpath, module_writer) -> None: ...
def _get_module_info_from_callable(callable_): ...
def _get_module_info(filename): ...
