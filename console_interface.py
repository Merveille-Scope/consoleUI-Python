# this is a test file.
# now testing only printing part.

import os
import json
import time

import division


lang = 'chinese'


class MainInterface(division.Interface):
    """
    i think the Interface also should be a specific type of Division.
    """
    def __init__(self):
        super(MainInterface, self).__init__()
        self.load_configure_and_resource()

        self._render_debug = True

    def load_configure_and_resource(self):
        # load resources
        res = json.load(open(os.path.join(os.path.split(__file__)[0],  # if you want resource in other dir, go change.
                                          'resources',
                                          'interface_res.json'),
                             encoding='utf-8'))
        self.interface_lang_dict = res[lang]


def auto_last_ops_time(caller):
    return "last operation time: %s" % time.ctime()


# test
if __name__ == "__main__":
    i = MainInterface()
    i.registry(division.Title(i.interface_lang_dict['title']))
    print(i.get_div_name())
    print("recursive depth:", i.get_recursive_depth())
    print("division ID:", i.get_div_id())

    b = division.Banner()
    b.set_help_message("press Enter to refresh")
    b.set_auto_brief_status(auto_last_ops_time)
    i.registry(b)
    print(b.get_div_name())
    print("recursive depth:", b.get_recursive_depth())
    print("division ID:", b.get_div_id())

    main_part = division.ContentDivision('str啊以')
    # print(main_part.get_cell_width())
    main_part.registry("\n\tthis is main part of the interface\n")
    # print(main_part.get_cell_width())
    i.registry(main_part)
    print(main_part.get_div_name())
    print("recursive depth:", main_part.get_recursive_depth())
    print("division ID:", main_part.get_div_id())

    c = division.CmdLine()
    c.registry('Enter your cmd: ')
    i.registry(c)
    print(c.get_div_name())
    print("recursive depth:", c.get_recursive_depth())
    print("division ID:", c.get_div_id())
    i.refresh()


