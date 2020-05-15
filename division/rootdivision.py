from .division import Division
from .division_exceptions import exceptions as e


class RootDivision(Division):
    _div_type_name = 'RootDivision'

    def set_parent_div(self, parent_div):
        raise e.RootDivisionError(self)
