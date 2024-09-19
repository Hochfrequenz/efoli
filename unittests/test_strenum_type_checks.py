from contextvars import ContextVar

from efoli import EdifactFormat, EdifactFormatVersion

my_format_context_var: ContextVar[EdifactFormat] = ContextVar("my_format_context_var", default=EdifactFormat.UTILMD)
my_version_context_var: ContextVar[EdifactFormatVersion] = ContextVar(
    "my_version_context_var", default=EdifactFormatVersion.FV2404
)
