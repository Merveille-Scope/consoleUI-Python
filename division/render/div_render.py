class Row:
    def __init__(self, *cells):
        self._cells = list(cells)  # these cells are division.
        self._height = 0
        self._width = 0
        self._calculate_height()
        self._calculate_width()

    def append(self, cell):
        self._cells.append(cell)
        self._calculate_height()
        self._calculate_width()

    def _calculate_width(self):
        self._width = 0
        for cell in self._cells:
            self._width += cell.size['width']

    @property
    def width(self):
        return self._width

    def _calculate_height(self):
        self._height = 0
        for cell in self._cells:
            self._height = cell.size['height'] if self._height < cell.size['height'] else self._height

    def height(self):
        return self._height


class Layout:
    def __init__(self):
        self.row_list = []


class Render:
    def __init__(self, div_instance, row_sep='|', line_sep=''):
        """
        :param div_instance: the div which initializes Render.
        :param row_sep: a pattern to separate two div in same line.
        :param line_sep: a pattern to separate div in next line.
        """
        self.div_instance = div_instance
        self.debug = self.div_instance._render_debug

    def render(self):
        return self.div_instance.print_div()


class ContainerRender(Render):
    def __init__(self, div_instance):
        super().__init__(div_instance)

    def render(self) -> str:
        """
        by calling render, it will return a formatted string.
        """
        _item_to_print = ''
        self._content_layout()
        return _item_to_print

    def _content_layout(self):
        container_size = self.div_instance.size
        contents_list = self.get_contents_list()
        self._content_row_layout(container_size, contents_list)

    def _content_row_layout(self, container_size, contents_list):
        # check if

        # content_lines: a list of content line.
        # a content_line contains content which are supposed to be aligned in one line.
        content_lines = []
        content_line = []
        line_width = container_size['width']
        # be careful that there's an "s".
        content_line_width = 0
        content_index = 0

        while content_index <= len(contents_list):
            content = contents_list[content_index]
            content_line_width += content['width']
            if content_line_width > container_size['width']:
                content_line.append(content)

    def get_contents_list(self):
        contents_size = []
        for content in self.div_instance._container:
            height = content.get_size('height')
            width = content.get_size('width')
            contents_size.append({'div': content, 'name': content.name, 'height': height, 'width': width})
        return contents_size


class ContentRender(Render):
    def __init__(self, div_instance):
        super().__init__(div_instance)
        self.content = self.div_instance._item_to_print
        self.max_size = self.div_instance.size

    def row_align(self):
        aligned_rows = self._adjust_content_to_max_width(self.content)
        self._then_adjust_to_max_height()

    def _adjust_content_to_max_width(self, content):
        max_width = self.max_size['width']

        return


    def _cut_in_lines(self):
        pass

    def _then_adjust_to_max_height(self):
        pass

    @staticmethod
    def _character_width(character):
        inside_code = ord(character)
        if inside_code > 255:
            chara_width = 2
        # still a problem: what if \t in the cell context?
        # should I raise an Exception?
        else:
            chara_width = 1
        return chara_width




