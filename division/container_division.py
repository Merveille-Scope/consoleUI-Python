from division.renderer import ContainerRenderer
from division.base_division import Division


class ContainerDivision(Division):
    def __init__(self, height: int, width: int, parent_division=None, **div_style):
        super().__init__(height, width, parent_division=None, **div_style)
        self._renderer = ContainerRenderer(height=height, width=width)

    def register(self, obj: Division):
        self._renderer.append_string_list(obj)

    def print_div(self, mode='format_string_list'):
        """
        or you might set mode='format_string' to get formatted string.
        """
        return self._renderer.render(mode)


