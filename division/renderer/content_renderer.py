from .renderer import Renderer
from .string_block import StringBlock


class ContentRenderer(Renderer):
    def __init__(self, height, width, **render_styles):
        """
        currently accepted styles:
        - trim: if set *True* that will make 

        it also accept *height* and *width*.
        """
        super().__init__(height, width, **render_styles)
        
        # when initialized, the string content is None.
        # if render
        self._string_content = None
        self._string_block = StringBlock(
            self._derived_string_block_size()['height'], 
            self._derived_string_block_size()['width']
        )
    
    def render(self, mode='format_string_list'):
        if mode == 'format_string_list':
            return self._string_block.format_string_list
        elif mode == 'format_string':
            return self._string_block.format_string_block
    
    def set_string_content(self, string_content: str):
        self._string_block.set_string_content(string_content)

    def set_render_style(self, **render_styles):
        """
        currently accepted styles:
        - trim: if set *True* that will

        it also accept *height* and *width*.
        """
        self._render_styles = render_styles

        self._string_block.set_block_styles(**self._derived_string_block_size())


if __name__ == '__main__':
    r = ContentRenderer(height=19, width=60, trim=True)
    string = """
        a string block will try to put character into a rectangle division.

        the unit of this rectangle's height is line. i.e. the height of a line on the console.

        the unit of the rectangles's width is half character. i.e. the width of a mono-spaced character.

        param:

        - height: height in lines.
        - width: width in half characters.

        block_styles:
        - h_trim: about how to trim columns if line count is greater than height.
            TODO: some style params about how to trim lines over the height.
        - w_trim: about how to trim rows if character count is greater than width.
            TODO: some style params about how to trim lines over the width.
        """
    r.set_string_content(string)

    print(r.render('format_string_list'))
    print(r.render('format_string'))

