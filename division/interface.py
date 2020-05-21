import platform
import json
import os

from .rootdivision import RootDivision


class Interface(RootDivision):
    _div_type_name = "Interface"

    def __init__(self):
        if platform.system() == 'Windows':
            self._clear_cmd = 'cls'
            self._path_separator = '\\'
        else:
            self._clear_cmd = 'clear'
            self._path_separator = '/'
        super().__init__()

    def refresh(self):
        os.system(self._clear_cmd)
        print(self.print_div())

    def print_div(self):
        self.style_console()
        return self._item_to_print

    def style_console(self):
        """
        basically how you want to print the main window.
        """
        self._item_to_print = '=' * (self._div_width if self._div_width else 80)

        self._item_to_print += '\n%s\n' % super(Interface, self).print_div()

        # self._item_to_print += '=' * (self._div_width if self._div_width else 80)  # bottom line is unnecessary.

    def load_configure_and_resource(self):
        """
        ```
        # load resources
        res = json.load(open(os.path.join(__file__[:__file__.rfind(self.path_separator)],
                                          'resources',
                                          'interface_res.json'),
                             encoding='utf-8'))
        self.interface_lang_dict = res[lang]
        ```
        for example.
        """
        pass

