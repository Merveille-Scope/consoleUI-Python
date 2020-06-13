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
        self._container = []
        self._separator = separator  # this is to divide two divisions in one line.

    def append_div(self, division):
        self._container.append(division)

    def render(self):
        # check div's display, if it's float, set in same line. if not, the next line.
        division_lines = []  # every line is expressed by a list called current_line.
        current_line = []
        for div in self._container:
            if div.styles and ['display'] in div.styles:
                # do something to put two divisions in one line.
                # remember to check if these two division is too wide to be in one line
                # in that case, put the division in next line.
                # don't forget to add separator between them.
                pass
            else:
                if current_line:
                    division_lines.append(current_line)
                    current_line = []  # must assign a new line, not clear.
                    # then go to the current line appending.
                    # appending current line should be a function.

    def _current_line_append(self, current_line, division):
        # this will check if the div could fit into current line.
        pass




        current_line = []
        division_lines = []
        available_width = self._render_styles['width']
        for div in self._container:
            if div.size['width'] <= available_width:  # if the width of the new div is able to fit in this line.
                current_line.append(div)
                available_width -= div.size['width']
            elif not self._container:

