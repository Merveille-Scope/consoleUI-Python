from division.base_division import Division
from division import renderer


class ContentDivision(Division):
    def __init__(self, height: int, width: int, parent_division=None, **div_style):
        super().__init__(height, width, parent_division=None, **div_style)
        self._renderer = renderer.ContentRenderer(height=height, width=width)

    def register(self, content):
        """
        usually string, sometimes ASCII draw?
        """
        self._renderer.set_string_content(content)

    def print_div(self, mode='format_string_list'):
        """
        or you might set mode='format_string' to get formatted string.
        """
        return self._renderer.render(mode)

    def get_string_block(self):
        return self._renderer

