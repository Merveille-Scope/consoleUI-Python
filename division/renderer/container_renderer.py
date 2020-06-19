from .renderer import Renderer
from .string_block.string_block import StringBlock

##
# listen, this class seems to getting too far from a simple class.
# it can handle an upper class such as division. this seems not right.
# it should only be able to handle string_block, and forming new string block.
##


class ContainerRenderer(Renderer):
    """
    this class deals with multiple division.
    the basic mechanism is:
        only deal with two divisions at the same time.
        two divisions should only have two types of relationships.
            one is in same line, another one is in different line.

        same line will cat string to the former string block.
        different line will append string lines at the bottom of the string block.
    """
    def __init__(self, height, width, separator=' | ', **render_styles):
        super().__init__(height, width, **render_styles)
        self._string_block_lines = []
        # the division line is a 2-dim list that shows alignment of divisions.
        # multiple lines could be in division lines. each line is a list of divisions.
        self._separator = separator  # this is to divide two divisions in one line.

    # definitely not smart operating string list in a renderer class.
    # should pass it to StringBlock

    def append_string_list(self, string_block: StringBlock, **styles):
        """
        :param string_block: the inserting StringBlock
        :param styles: display='float' means it will try to be inserted in the same line.
        """
        if styles.get('display') == "float":
            # TODO: check if obj's width is available to be inserted into the same line.
            if self._string_block_lines and self._insertable_by_width(string_block.size['width']):
                self._same_line_append(string_block)
            else:
                self._next_line_append(string_block)
        else:
            self._next_line_append(string_block)

    def _same_line_append(self, string_block: StringBlock):
        """
        this method tries to append a string block at the same division line.
        """
        self._string_block_lines[-1]['string_list'].append(string_block)
        self._string_block_lines[-1]['width'] += (StringBlock.string_length(self._separator) + string_block.size['width'])

    def _next_line_append(self, string_block: StringBlock):
        """
        this will simply append the string list to the next division line.
        """
        # some StringBlock appending i guess
        self._string_block_lines.append({'string_list': [string_block], 'width': string_block.size['width']})

    def _insertable_by_width(self, inserting_line_width):
        # note to me: no need to measure the string list's appeared width.
        # because it must equal to the division it belongs to.
        # but still StringBlock.string_length() is necessary...

        # first, get the available width of the last div line, or current div line.
        total_div_line_width = self._render_styles['width']
        separator_width = StringBlock.string_length(self._separator)
        current_line_width = self._string_block_lines[-1]['width']
        available_width = total_div_line_width - current_line_width - separator_width
        # sub by a separator because inserting new div will add a separator.
        if available_width >= 0:
            return True
        else:
            return False

    def render(self, mode):
        if mode == 'format_string_list':
            return self.format_string_list
        elif mode == 'format_string':
            return self.format_string

    @property
    def format_string_list(self) -> list:
        string_list = []
        while self._string_block_lines:
            current_string_block_line = self._string_block_lines.pop(0)
            current_line_string_list = self._align_current_stringblock_line_into_string_list(current_string_block_line)
            for line in current_line_string_list:
                string_list.append(line)
        return string_list

    @property
    def format_string(self) -> str:
        return '\n'.join(self.format_string_list)




