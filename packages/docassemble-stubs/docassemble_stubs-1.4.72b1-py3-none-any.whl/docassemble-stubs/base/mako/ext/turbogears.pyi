from _typeshed import Incomplete
from docassemble.base.mako import compat as compat
from docassemble.base.mako.lookup import TemplateLookup as TemplateLookup
from docassemble.base.mako.template import Template as Template

class TGPlugin:
    extra_vars_func: Incomplete
    extension: Incomplete
    lookup: Incomplete
    tmpl_options: Incomplete
    def __init__(self, extra_vars_func: Incomplete | None = ..., options: Incomplete | None = ..., extension: str = ...) -> None: ...
    def load_template(self, templatename, template_string: Incomplete | None = ...): ...
    def render(self, info, format: str = ..., fragment: bool = ..., template: Incomplete | None = ...): ...
