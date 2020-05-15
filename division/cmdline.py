from .division import Division
from .division_exceptions import exceptions as e


class CmdLine(Division):
    _div_type_name = "CmdLine"

    def _registry_div(self, div, callback=None, *args):
        raise e.NotContainerError(self)
