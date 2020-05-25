# base class of division
from .division_exceptions import exceptions as e
from .render import ContainerRender, ContentRenderer


MAXIMUM_DIV_COUNT = 1000
render_debug_mode = False  # if set True, any overflow or some other unexpected situation will print themselves out.


class Division:
    div_count = 0
    _div_type_name = "Division"

    _render_debug = render_debug_mode

    display = 'block'  # or you can set it 'float'.

    def __init__(self, parent_div=None, **other_parameters):
        global MAXIMUM_DIV_COUNT
        if Division.div_count < MAXIMUM_DIV_COUNT:
            Division.div_count += 1
        else:
            raise e.TooManyDivisionsError(MAXIMUM_DIV_COUNT)

        self._div_layer = 0
        # if it's 0, means this div is brand new layer.
        # if it's 1, means this div has no parent division. it's root division.
        # if it's 2, means this div has a parent division. the parent division is the root division.

        self.selectable = False  # if set selectable, an item number should appear.

        # if div id is 0, means it has not gotten an id. if gets registered, _auto_div_id() will be called.
        self._div_id = 0 if 'id' not in other_parameters else other_parameters['id']

        self._parent_div = parent_div

        self._item_to_print = ''

        self._div_name = None if 'name' not in other_parameters else other_parameters['name']

        # if any of these two were set 0, means it or both are not limited
        # the max lines THIS div should occupy, in lines
        self._div_height = 0 if 'height' not in other_parameters else other_parameters['height']
        # the max width THIS div should occupy, in characters
        self._div_width = 0 if 'width' not in other_parameters else other_parameters['width']

        self._container = []  # child divisions will be print

    #############################
    #    division attributes    #
    #############################
    def set_div_name(self, name):
        if name:
            self._div_name = name
        else:
            self._auto_div_name()

    def _auto_div_name(self):
        self._div_name = '%s<%s>' % (self._div_type_name, self._div_id)

    def get_div_name(self):
        if self._div_name:
            return self._div_name
        else:
            self._auto_div_name()
            return self._div_name

    def name(self):
        return self._div_name

    def get_parent_div(self):
        return self._parent_div

    def get_recursive_depth(self, *args):
        # if div layer is not 0, that means this div must have calculated the layer.
        if self._div_layer and '-f' not in args:
            return self._div_layer
        else:
            self.force_calculate_layer()
            return self.get_recursive_depth()

    def force_calculate_layer(self):
        if self._parent_div:
            self._div_layer = self._parent_div.get_recursive_depth('-f') + 1
        else:  # no parent div, it's root div.
            self._div_layer = 1

    def auto_div_id(self):
        """
        id rule:
        the root div has ID = 0
        other div in root div will have id started from 1000.

        no more than 999 divs can be in the window.
        well if you just want it to excess 999, change the number below.
        """
        global MAXIMUM_DIV_COUNT
        self._div_id = (Division.div_count-1) + MAXIMUM_DIV_COUNT * (self.get_recursive_depth() - 1)

    def get_div_id(self):
        return self._div_id

    def set_parent_div(self, parent_div):
        self._parent_div = parent_div

    def set_size(self, **height_or_width_in_int: int):
        if 'height' in height_or_width_in_int:
            self._div_height = height_or_width_in_int['height']
        if 'width' in height_or_width_in_int:
            self._div_width = height_or_width_in_int['width']

    def get_size(self, dimension: str = None):
        if dimension in ('height', 'width'):
            return self._div_width if dimension == 'width' else self._div_height
        else:
            return {"height": self._div_height, "width": self._div_width}

    @property
    def size(self):
        return self.get_size()

    #############################
    #     division content      #
    #############################
    def clear_content(self):
        self._item_to_print = ''
        self._container.clear()

    def registry(self, obj, callback=None, *callback_args, **div_params):
        """
        if obj is string or other Object, registry it as content. if not, as division.

        if Division is registered, this div will treat itself a container.

        container will show no string hold by itself, it will display child divs instead.
        :param obj: whatever object that can be print or a Division object.
        :param callback: callback function to format the obj.
        :param callback_args: these args is going to pass to the callback.
        :param div_params: anything about the registering div.
        :return:
        """
        if isinstance(obj, Division):
            self._registry_div(obj, callback, *callback_args)
        else:
            self._registry_content(obj, callback, *callback_args)

    def _registry_content(self, content, callback=None, *args):
        """
        it will try to format a content to fill the division.
        :param content: object that needs to be printed in the division.
        :param callback: if given, callback(content, *args) should return a formatted string.
        :param args: will be args passed to the callback.
        :return: None
        """
        if callback:
            self._item_to_print = callback(content, *args)
        else:
            self._item_to_print = content.__str__()

    def _registry_div(self, div, callback=None, *args):
        self._container.append(div)
        div.set_parent_div(self)
        div.force_calculate_layer()
        div.auto_div_id()
        if self._item_to_print:
            self._item_to_print += "\n%s. %s" % (len(self._container), div)
        else:
            self._item_to_print += "1. %s" % div

    def print_div(self):
        """
        but using either ContainerDiv or ContentDiv is encouraged.
        """
        # print("debug: %s.print_div()" % id(self))
        if self._container:
            return self._container_rendering()
        else:
            return self._div_rendering()

    def _container_rendering(self):
        """
        this should try to format all div in the container.
        :return: formatted div string
        """
        # self._content_render = ContainerRender(self)
        rendered_div_string = ''
        for div in self._container:
            if rendered_div_string:
                rendered_div_string += "\n%s" % div.print_div()
            else:
                rendered_div_string += "%s" % div.print_div()
        return rendered_div_string

    def _div_rendering(self):
        """
        consider this div is a string type div.
        :return: formatted div string
        """
        # self._content_render = ContentRender(self)  # not sure what to do with this.
        return self._item_to_print if self._item_to_print else "empty division: %s" % self.get_div_name()
        # i need a formatter class to automatically handle with ordinary object.

    def __repr__(self):
        """
        if self._container is not empty, this Division treat itself a _container.

        i.e. any div in self._container will override any string in it.

        :return: str
        """
        obj_name = "%s id=%s" % (type(self), id(self))
        if self._container:
            return "%s is a _container.\ncontent list:\n%s" % (obj_name, self._item_to_print)
        else:
            return self._item_to_print if self._item_to_print else "empty division: %s" % obj_name


class ContentDivision(Division):
    def __init__(self, parent_div=None, **other_parameters):
        super().__init__(parent_div, **other_parameters)
        self.content_render = ContentRenderer(self.get_raw_content(), self._render_debug, self)

    def _registry_div(self, div, callback=None, *args):
        raise e.NotContainerError(self)

    def get_raw_content(self):
        return self._item_to_print

    def print_div(self) -> list:
        """
        this method would return list of lines.
        """
        return self._div_rendering()

    def _div_rendering(self):
        return self.content_render._get_string_list()


class ContainerDivision(Division):
    def __init__(self, parent_div=None, **other_parameters):
        super().__init__(parent_div, **other_parameters)
        self._content_render = ContainerRender(self)

    def _registry_content(self, content, callback=None, *args):
        raise e.ContainerError(self)

    def get_raw_content_list(self):
        return self._container

    def print_div(self):
        return self._container_rendering()

    def _container_rendering(self):
        """
        this should try to format all div in the container.
        :return: formatted div string
        """
        return self._content_render.get_format_string_block()


# this are just test.
# even the div_height and div_width are not in use.
#


if __name__ == "__main__":
    d1 = Division(height=0, width=0)


    class StringTestClass:
        string = "this is a test string object"

        def __str__(self):
            return self.string


    d1.registry("this is div1")
    d2 = Division(height=0, width=0)
    d2.registry(StringTestClass())
    d3 = Division(height=0, width=0)
    d3.registry(d1)
    d3.registry(d2)
    print("==== d1 ====")
    print(d1)
    print(d1.print_div())
    print("==== d2 ====")
    print(d2)
    print(d2.print_div())
    print("==== d3 ====")
    print(d3)
    print(d3.print_div())

    # for empty div.
    print("==== d4 ====")
    d4 = Division(height=0, width=0)
    print(d4)
    print(d4.print_div())
