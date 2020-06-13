# implement of renderers
# 
# renderer solves if in any case that you want to show the string in a box.


class Renderer:
    def __init__(self, height, width, **render_styles):
        # in order to access the attributes of the instance 
        # which this renderer belong to.
        self._render_styles = render_styles
        self._render_styles['height'] = height
        self._render_styles['width'] = width

    def render(self):
        raise NotImplementedError(
            "%s is an abstract class, you should either use ContentDivision or ContainerDivision to make it work." 
            % type(self)
        )

    def _derived_string_block_size(self) -> dict:
        # TODO: i might want to deal with if this Render wants a "box"
        # the box means something like this:
        # +---------+
        # |   box   |
        # +---------+
        # thus the actual size of string block might be less than the div.

        d = dict()
        d['height'] = int(self._render_styles['height'])
        d['width'] = int(self._render_styles['width'])
        return d
