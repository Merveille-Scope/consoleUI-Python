# implement of _title div
from typing import Callable


from .division import Division
from .division_exceptions import exceptions


class Title(Division):
    """
    specialized Division, which helps fast form a title division.
    """

    _div_type_name = 'Title'

    def __init__(self, title_string: str,
                 style: str = 'default',
                 style_format: Callable = None,
                 *callback_args,
                 **other_parameters
                 ):
        self._title = title_string
        self._style = style
        self._callback_format = style_format if callable(style_format) else None
        self._callback_args = callback_args

        super(Title, self).__init__()

    def set_parent_div(self, parent_div):
        super().set_parent_div(parent_div)
        self.set_size(**self._parent_div.get_size())
        self._title_format()

    def _title_format(self):
        if not self._parent_div:
            raise exceptions.NoParentDivisionError(self)

        if self._callback_format:
            self._item_to_print = self._callback_format(self._title, *self._callback_args)
        else:
            if self._style == 'default':
                self._item_to_print = "%s\n" % self._title
                if self._div_width:
                    self._item_to_print += '-' * self._div_width
                else:
                    self._item_to_print += '-' * 80

    def _registry_div(self, div, callback=None, *args):
        raise exceptions.NotContainerError(self)


# test.
if __name__ == "__main__":
    p_div = Division()
    title = Title('Test title')
    p_div.registry(title)
    print(p_div.print_div())
