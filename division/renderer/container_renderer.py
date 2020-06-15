from .renderer import Renderer

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
        self._division_lines = []  # a list of string line.
        # the division line is a 2-dim list that shows alignment of divisions.
        # multiple lines could be in division lines. each line is a list of divisions.
        self._separator = separator  # this is to divide two divisions in one line.

    def append_string_list(self, string_list, **styles):
        if styles.get('display') == "float":
            self._same_line_append(string_list)
        else:
            self._next_line_append(string_list)

    def _same_line_append(self, string_list):
        """
        this method tries to append a string block at the same division line.
        """
        if self._division_lines:
            self._division_lines[-1].append(string_list)
        else:
            self._division_lines.append([string_list])

    def _next_line_append(self, string_list):
        """
        this will simply append the string list to the next division line.
        """
        self._division_lines.append([string_list])

    def render(self, mode):
        if mode == 'format_string_list':
            return  self.format_string_list
        elif mode == 'format_string':
            return  self.format_string

    @property
    def format_string_list(self):
        string_block_list = []
        while self._division_lines:
            current_div_line = self._division_lines.pop(0)
            self._align_current_div_line
        return

    @@property
    def format_string(self):
        return




