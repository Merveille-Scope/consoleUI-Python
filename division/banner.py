# implement of division banner
from typing import Callable

from .division import Division
from .division_exceptions import exceptions as e


class Banner(Division):
    """
    this class would work as a banner which follows right after Title.

    it should display brief help and brief status.
    """
    _div_type_name = 'Banner'

    def __init__(self):
        super().__init__()
        self._help_message = ''
        self._brief_status = ''
        self._auto_get_brief_status = None

    def set_help_message(self, message):
        self._help_message = message

    def set_brief_status(self, status):
        self._brief_status = status

    def set_auto_brief_status(self, get_status_callback: Callable):
        """
        by given the callback to auto_brief_status, no more set_status() should be called.

        this callback **MUST** have the first position arg which is the caller Division.

        because in some situation, you want to also update other part of the division such as self.set_help_message().

        the callback will be called at when brief_status() is called, and self will pass to it as first pos arg.

        i.e. self._auto_get_brief_status(self)

        :param get_status_callback: a function that has first position arg which is the caller division.
        """
        self._auto_get_brief_status = get_status_callback

    @property
    def brief_status(self):
        if self._auto_get_brief_status:
            if callable(self._auto_get_brief_status):
                self._brief_status = self._auto_get_brief_status(self)  # because callback should know who calls it.
                return self._brief_status
            else:
                raise e.NoCallbackAvailableError(self, self._auto_get_brief_status)
        else:
            return self._brief_status

    def clear_content(self):
        self._brief_status = ''
        self._auto_get_brief_status = None
        self._help_message = ''
        self._item_to_print = ''

    def print_div(self):
        self._item_to_print = self.brief_status + '\n' + self._help_message
        return self._item_to_print

    def _registry_div(self, div, callback=None, *args):
        raise e.NotContainerError(self)

