try:
    from .division import ContainerDivision, ContentDivision
    from .division_exceptions import exceptions as e
except ImportError:
    from division.division import ContentDivision, ContainerDivision


class TableCell(ContentDivision):
    _div_type_name = "TableCell"

    def __init__(self, cell_content, callback=None, *callback_args, **cell_style):
        """
        cell_content accept only string or object has __str__() method.
        """
        super().__init__()

        self.registry(cell_content, callback, *callback_args, **cell_style)
        self.set_cell_style(**cell_style)

        # the problem here is to determine the size of a cell.
        # a cell can have width limiting the length which keeps the table formatted.
        # a cell can of course have height, too.

    def set_cell_style(self, **cell_style):
        self._cell_separator = cell_style['sep'] if 'sep' in cell_style else '\t'
        if self._item_to_print.find(self._cell_separator) != -1:
            raise e.SeparatorError(self)
        self._cell_align = cell_style['align'] if 'align' in cell_style else 'left'
        self._cell_height = cell_style['height'] if 'height' in cell_style else 1  # height would be 1 by default.
        self._cell_width = cell_style['width'] if 'width' in cell_style else 0  # 0 by default, means no limited.

        self._render_cell()

    @property
    def cell_separator(self):
        return self._cell_separator

    def _render_cell(self):
        # called in self.set_cell_style()
        # every time the cell style is changed, the cell should be rendered.
        pass

    # this method should be changed into another name.
    # or it'll finally become a Division method.
    def get_cell_width(self):
        width = 0
        for char in self._item_to_print:
            width += self._character_width(char)
        return width

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


class TableRow(ContainerDivision):
    is_header_row = False
    _div_type_name = "TableLine"


class Table(ContainerDivision):
    _div_type_name = "Table"

    def registry(self, obj: TableRow, callback=None, *callback_args, **div_params):
        """
        obj accept only TableLine.

        each TableLine should have same count of fields,

        if not, empty field will be filled by blank space.

        style parameters are:

            - margin_top: top margin, accept one character. '#' by default.

            - margin_bottom: '#' by default.

            - margin_left: not available now, but '#' by default.

            - margin_right: not available now, but '#' by default.

            - header_line_sep: '-' by default.

            - header_row_sep: '|' by default.

        """
        super().registry(obj, callback, *callback_args, **div_params)
        if obj.is_header_row:
            header = self._container.pop()
            self._container.insert(0, header)


