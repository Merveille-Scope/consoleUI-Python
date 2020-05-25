# base class of division
from .division_exceptions import exceptions as e
from .render import ContainerRender, ContentRenderer

# from division_exceptions import exceptions as e
# from render import ContainerRender, ContentRenderer

MAXIMUM_DIV_COUNT = 1000
render_debug_mode = False  # if set True, any overflow or some other unexpected situation will print themselves out.


class Division:
    div_count = 0
    _div_type_name = "BaseDivision"

    _render_debug = render_debug_mode

    # display = 'block'  # or you can set it 'float'.

    def __init__(self, parent_div=None, **div_parameters):
        """
        div parameters would have everything that a division want to have.
        div_parameters = {
            'parent_div': None,

            'display': 'block',

            'width': 80,
            'height': 24,

            'container': [],  # whatever divs you want to put into the div.
            # the container will override content.
            # i.e. if some thing in container, content will be ignored.
            'content': "",  # usually some string.
            # it can also be a __str__() object.
            # when this div needs to be printed,
            # container or content would be passed into render and return formatted string block.

            # string block:
            #   a class that if you index will return a string line, __str__() will return formatted string.
            #   for details see ./render/div_render.py

            # if selectable, then the object must have method call(),
            # and must be able to express itself by *some method*. for when as a division. TODO: method name required.
            # and it might want to show detailed information on main part of the interface,
            # thus, it might need some way to handle the division things.
            # which indicates that division should be able to handle a set of divisions' init() in one call.
            #   and if possible, using some expressions to make it.
            'selectable': False,
            'object': None
        }
        """
        global MAXIMUM_DIV_COUNT
        if Division.div_count < MAXIMUM_DIV_COUNT:
            Division.div_count += 1
        else:
            raise e.TooManyDivisionsError(MAXIMUM_DIV_COUNT)

        self._div_layer = 0
        # if it's 0, means this div is brand new layer.
        # if it's 1, means this div has no parent division. it's root division.
        # if it's 2, means this div has a parent division. the parent division is the root division.

        self.selectable = False if 'selectable' not in div_parameters else div_parameters['selectable']
        # if set selectable, an item number should appear.

        # if div id is 0, means it has not gotten an id. if gets registered, _auto_div_id() will be called.
        self._div_id = 0 if 'id' not in div_parameters else div_parameters['id']

        self._parent_div = parent_div if 'parent_div' not in div_parameters else div_parameters['parent_div']

        self._div_name = None if 'name' not in div_parameters else div_parameters['name']

        # TODO: if any of these two were set 0, means it or both are not limited.
        # TODO: how about 'auto' to fit the size of parent div?

        # the max lines THIS div should occupy, in lines
        if 'height' not in div_parameters:
            if self._parent_div:
                div_parameters['height'] = self._parent_div.size['height']
                self._div_height = self._parent_div.size['height']
            else:
                self._div_height = 24
                div_parameters['height'] = 24
        else:
            self._div_height = div_parameters['height']
        # the max width THIS div should occupy, in characters
        if 'width' not in div_parameters:
            if self._parent_div:
                div_parameters['width'] = self._parent_div.size['width']
                self._div_width = self._parent_div.size['width']
            else:
                self._div_width = 80
                div_parameters['width'] = 80
        else:
            self._div_width = div_parameters['width']

        self._display = div_parameters['display'] if 'display' in div_parameters else 'block'

        self._container = [] if 'container' not in div_parameters else div_parameters['container']
        self._content = None if 'content' not in div_parameters else div_parameters['content']

        self._renderer = None  # should be inited when something get registered.
        # self._item_to_print = ''  # deprecated
        self._div_style = div_parameters  # this is finally here, designed for division renderer.

    #############################
    #    division attributes    #
    #############################

    # division name ######################
    def set_div_name(self, name):
        if name:
            self._div_name = "%s<%s>" % (name, self._div_id)
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

    @property
    def name(self):
        return self._div_name

    # division structure ###################
    def set_parent_div(self, parent_div):
        if self._parent_div:
            raise e.ParentDivisionError(self)
        self._parent_div = parent_div
    # TODO: what if the parent div calls clear_content()? should all child div be removed or set parent_div None?

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

    # division ID #####################
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

    # division attributes ###################
    def set_size(self, **height_or_width_in_int: int):
        if 'height' in height_or_width_in_int:
            self._div_height = height_or_width_in_int['height']
        if 'width' in height_or_width_in_int:
            self._div_width = height_or_width_in_int['width']
        if self._renderer:
            self._renderer.set_size(**height_or_width_in_int)

    def get_size(self, dimension: str = None):
        if dimension in ('height', 'width'):
            return self._div_width if dimension == 'width' else self._div_height
        else:
            return {"height": self._div_height, "width": self._div_width}

    @property
    def size(self):
        return self.get_size()

    @property
    def display(self):
        return self._display

    def set_div_style(self, **styles):
        # TODO: if any of these two were set 0, means it or both are not limited)
        # the max lines THIS div should occupy, in lines
        self._div_height = self._div_height if 'height' not in styles else styles['height']
        # the max width THIS div should occupy, in characters
        self._div_width = self._div_width if 'width' not in styles else styles['width']
        self._display = self._display if 'display' not in styles else styles['display']

    #############################
    #     division content      #
    #############################
    def clear_content(self):
        # self._item_to_print = ''
        self._content = None
        # TODO: maybe need to recursively wipe all child div's parent_div.
        self._container.clear()

    def registry(self, obj):
        """
        if obj is string or other Object, registry it as content. if not, as division.

        if Division is registered, this div will treat itself a container.

        container will show no string hold by itself, it will display child divs instead.
        :param obj: whatever object that can be print or a Division object.
        # :param callback: callback function to format the obj.  # disabled.
        # :param callback_args: these args is going to pass to the callback.  # disabled

        # :param div_params: anything about the registering div.
        # deprecated, the division info can be accessed by api from
        :return:
        """
        if issubclass(type(obj), Division):
            self._registry_div(obj, **self._div_style)
        else:
            self._registry_content(obj, **self._div_style)

    def _registry_content(self, content, **styles):
        """
        it will try to format a content to fill the division.
        :param content: object that needs to be printed in the division.
        :param callback: if given, callback(content, *args) should return a formatted string.
        :param args: will be args passed to the callback.
        :return: None
        """
        self._content = content
        self._renderer = ContentRenderer(self._content, self._render_debug, **self._div_style)

        self._auto_div_name()

    def _registry_div(self, div, **styles):
        self._container.append(div)
        div.set_parent_div(self)
        div.force_calculate_layer()
        div.auto_div_id()

        self._renderer = ContainerRender(self._container, self._render_debug, **self._div_style)

        self._auto_div_name()

    #############################
    #     division printing     #
    #############################
    def print_div(self):
        """
        but using either ContainerDiv or ContentDiv is encouraged.
        """
        # print("debug: %s.print_div()" % id(self))
        # if self is the RootDivision:
        if self._parent_div is None:
            return self._renderer.string_block
        else:
            return self._renderer.string_list

    def __repr__(self):
        """
        if self._container is not empty, this Division treat itself a _container.

        i.e. any div in self._container will override any string in it.

        :return: str
        """
        self_name = "%s id=%s" % (self.name, id(self))
        if self._container:
            return "%s is a _container.\ncontent list:\n%s" % (self_name, self._container)
        else:
            return "division: %s" % self_name


class ContentDivision(Division):
    def __init__(self, parent_div=None, **div_parameters):
        super().__init__(parent_div, **div_parameters)
        # self.content_render = ContentRenderer(self._content, self._render_debug, **self._div_style)

    def registry(self, obj):
        """
        if obj is string or other Object, registry it as content. if not, as division.

        if Division is registered, this div will treat itself a container.

        container will show no string hold by itself, it will display child divs instead.
        :param obj: whatever object that can be print or a Division object.
        # :param callback: callback function to format the obj.  # disabled.
        # :param callback_args: these args is going to pass to the callback.  # disabled

        # :param div_params: anything about the registering div.
        # deprecated, the division info can be accessed by api from
        :return:
        """
        self._registry_content(obj, **self._div_style)

    def _registry_div(self, obj, **div_styles):
        raise e.NotContainerError(self)

    def get_raw_content(self):
        return self._item_to_print


class ContainerDivision(Division):
    def __init__(self, parent_div=None, **div_parameters):
        super().__init__(parent_div, **div_parameters)

    def _registry_content(self, content, callback=None, *args):
        raise e.ContainerError(self)

    def get_raw_content_list(self):
        return self._container


# this are just test.
# even the div_height and div_width are not in use.
#


if __name__ == "__main__":
    d1 = Division()


    class StringTestClass:
        string = "this is a test string object"

        def __str__(self):
            return self.string


    d1.registry("this is div1")
    d2 = Division()
    d2.registry(StringTestClass())
    d3 = Division()
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
    d4 = Division()
    print(d4)
    print(d4.print_div())
