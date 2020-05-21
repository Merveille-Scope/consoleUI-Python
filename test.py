# this is a test file.
# now testing only printing part.

import os
import json
import time

import division


lang = 'chinese'


class TestInterface(division.Interface):
    """
    i think the Interface also should be a specific type of Division.
    """
    def __init__(self):
        super(TestInterface, self).__init__()
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
    i = TestInterface()
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

    main_part = division.ContentDivision()
    main_part.set_size(height=20, width=30)
    # print(main_part.get_cell_width())
    # main_part.registry("\n\tthis is main part of the interface\n")
    register_string = '对我个人而言，人类之光连裤袜不仅仅是一个重大的事件，还可能会改变我的人生。' \
                        '就我个人来说, 人类之光连裤袜对我的意义, 不能不说非常重大. 本人也是经过了深思熟虑,在每个日日夜夜思考这个问题.'\
                        '克劳斯·莫瑟爵士在不经意间这样说过 : 教育需要花费钱，而无知也是一样。'\
                        '所谓人类之光连裤袜, 关键是人类之光连裤袜需要如何写. 洛克曾经提到过 : 学到很多东西的诀窍，就是一下子不要学很多。'\
                        '带着这句话, 我们还要更加慎重的审视这个问题: 我认为, 在这种困难的抉择下, 本人思来想去, 寝食难安.'\
                        '可是，即使是这样，人类之光连裤袜的出现仍然代表了一定的意义。 '
    main_part.registry(register_string)
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


# TODO: the calling path has become a chaos. must reform the division. remove useless derived class.
# TODO: once the base Container and Content Division are finished, rewrite special div such as Title, Banner.

