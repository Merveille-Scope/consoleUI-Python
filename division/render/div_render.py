class Render:
    def __init__(self, content, render_debug, **div_styles):
        """
        :param render_debug: if it needs to print any debugging information.
        :param div_styles: about div size, separators and others.
        """
        self.div_styles = div_styles
        self.debug = render_debug
        self.content = content
        self.width = div_styles['width'] if 'width' in div_styles else 0
        self.height = div_styles['height'] if 'height' in div_styles else 0

    def set_size(self, **height_or_width_in_int: int):
        self.width = self.width if 'width' not in height_or_width_in_int else height_or_width_in_int['width']
        self.height = self.height if 'height' not in height_or_width_in_int else height_or_width_in_int['height']

    ########################################################################################
    #   two static methods to measure length of a character/string appearing on console.   #
    ########################################################################################
    @staticmethod
    def string_length(string):
        length = 0
        for char in string:
            length += ContentRenderer.character_width(char)
        return length

    @staticmethod
    def character_width(character):
        # only considering ASCII characters, please don't make strange things in it.
        inside_code = ord(character)
        if inside_code > 255:
            chara_width = 2
        # still a problem: what if \t in the cell context?
        # update: the content string has .replace() "\n" and "\t" into " " and "    ".
        else:
            chara_width = 1
        return chara_width

    def _get_string_list(self) -> list:
        content_string = self.content.__str__()
        string_lines = self._format_content_according_to_width(content_string)
        string_lines = self._format_content_according_to_height(string_lines)
        string_lines = self._fill_last_line(string_lines)

        return string_lines

    def _get_string_block(self) -> str:
        content_string = self.content.__str__()
        string_lines = self._format_content_according_to_width(content_string)
        string_lines = self._format_content_according_to_height(string_lines)
        string_lines = self._fill_last_line(string_lines)
        string_block = ''
        for line in string_lines:
            if string_block:
                string_block += '\n'
            string_block += line
        return string_block

    #
    #   some mysterious methods which process given string paragraph into
    #
    def _format_content_according_to_width(self, content_string):
        char_lines = self._cut_string_in_char_lines(content_string)
        string_lines = []
        for char_line in char_lines:
            line = ''
            for char in char_line:
                line += char
            string_lines.append(line)
        return string_lines

    def _format_content_according_to_height(self, string_lines):
        div_height = self.height
        total_lines = len(string_lines)
        if total_lines > div_height:
            string_lines = string_lines[:div_height - 1]
            folding_info = "%s more line(s) folded..." % (total_lines - div_height)
            if self.width >= self.string_length(folding_info):
                string_lines.append(folding_info)
            elif self.width >= 3:
                string_lines.append('...')
            else:
                string_lines.append('~')
        return string_lines

    def _fill_last_line(self, string_lines):
        # the last line needs to be filled with ' '
        last_line_length = self.string_length(string_lines[-1])
        div_width = self.width
        if last_line_length < div_width:
            spaces_to_fill = div_width - last_line_length
            string_lines[-1] += ' ' * spaces_to_fill
        return string_lines

    def _cut_string_in_char_lines(self, string):
        """
        this method cut raw string content into a list of single characters.
        """
        string = string.replace("\n", " ").replace("\t", "    ")
        # invisible chars like "\n" and "\t" are not expected, because their length on console is hard to express.

        max_line_width = self.width
        total_length = self.string_length(self.content.__str__())

        char_list = list(self.content.__str__())
        char_lines = []  # list of character_lists, each character_list contains characters in one line.
        char_line = []  # single line of characters.
        current_line_width = 0
        while char_list:
            next_char = char_list.pop(0)
            char_width = self.character_width(next_char)
            if current_line_width + char_width > max_line_width:
                if current_line_width == max_line_width:
                    char_lines.append(char_line)
                    char_line = []
                    char_line.append(next_char)
                    current_line_width = self.character_width(next_char)
                else:
                    char_line.append(' ')
                    char_lines.append(char_line)
                    char_line = []
                    char_line.append(next_char)
                    current_line_width = self.character_width(next_char)
            else:
                current_line_width += char_width
                char_line.append(next_char)
        else:
            if char_line:
                char_lines.append(char_line)

        return char_lines

        ###################################
        #   output string lines in list   #
        ###################################
    @property
    def string_list(self):
        return self._get_string_list()

    @property
    def string_block(self):
        return self._get_string_block()


class ContentRenderer(Render):
    # content = ""
    # max_size = {'height': 24, 'width': 80}

    def __init__(self, content, render_debug, **div_styles):
        """
        the style params accepts some style control parameters.
            height
            width

            one_line: shrink the content to 1 line. if string length is greater than width, trim the line to fit width.
                one_line=True or whatever value that might be taken as True will be accepted.
            trim_line: must give value in integer. will cut every line before formatted content returns.
                example:
                    [
                        'string line 1.',
                        'string line 2.'
                    ]
                    when trim_line=4:
                    [
                        'string lin',
                        'string lin'
                    ]
                    when trim_line=-2:
                    [
                        'ring line 1.',
                        'ring line 2.'
                    ]
        """
        super().__init__(content, render_debug, **div_styles)


class ContainerRender(Render):
    def __init__(self, content_list, render_debug, row_sep='|', line_sep='', **div_styles):
        content = content_list
        super().__init__(content, render_debug, **div_styles)
        self._row_sep = row_sep
        self._line_sep = line_sep

    def get_format_content(self) -> list:
        """
        returns a list of lines (which is called "string block") that can be directly print line.
        this list should be like:

        [
            'div1 string SEP div2 string',
            'div1 BLANK  SEP div2 string',
            'BLANK FILL  SEP div2 BLANK '
        ]
        the BLANK and FILL are simply space to fill the division.
        SEP is separator. the SEP is ' | ' by default.
        """
        # first, determine divs in container that are in the same "division line".
        div_lines = self._form_div_lines()

        # calculate height and width for each line.
        # here's a problem:
        #   need to find a way to either cut the div or put the div to next line
        #   if the total width is greater than max width of their parent division.
        div_line_info = self._calculate_line_height_and_width(div_lines)

        # format a string block.
        string_block = self._format_string_block(div_line_info)
        return string_block

    def get_format_string_block(self):
        string_block = self.get_format_content()

        # prepare lines
        string_block_list = []
        for line in string_block:
            string = ''
            for sub_string in line:
                if string:
                    string += self._row_sep
                string += sub_string
            string_block_list.append(string)

        # fill the block with space.
        line_index = 0
        while line_index < len(string_block_list):
            string_length = self.string_length(string_block_list[line_index])
            if string_length < self.width:
                string_block_list[line_index] += ' ' * (self.width - string_length)
            line_index += 1
        return string_block_list

    def _form_div_lines(self):
        container = self.content
        current_line = []
        div_lines = []
        for div in container:
            if len(current_line) == 0:
                current_line.append(div)
            elif div.display == 'float':
                current_line.append(div)
            else:
                div_lines.append(current_line)
                current_line = [div]
        else:
            div_lines.append(current_line)
        return div_lines

    def _calculate_line_height_and_width(self, div_lines):
        """
        returns a list of Division Line.
        a Division Line is a dict looks like:
            {
                'width': 20, 'height': 5, 'divs': [Division1, Division2 ...]
            }
        """
        div_lines_with_info = []
        for div_line in div_lines:
            one_line_info = {}
            one_line_info['width'] = self._calculate_line_width(div_line)
            one_line_info['height'] = self._calculate_line_height(div_line)
            one_line_info['divs'] = div_line
            div_lines_with_info.append(one_line_info)
        return div_lines_with_info

    def _calculate_line_width(self, line):
        line_width = 0
        for div in line:
            if line_width:
                line_width += self.string_length(self._row_sep)  # separator occupies rooms.
            line_width += div.size['width']
        return line_width

    def _calculate_line_height(self, line):
        line_height = 0
        for div in line:
            div_height = div.size['height']
            line_height = div_height if div_height > line_height else line_height
        return line_height

    def _format_string_block(self, div_line_info):
        string_block = []

        # get total height, then prepare empty lines for string block.
        div_line_count = 0
        for div_line in div_line_info:
            div_line_count += div_line['height']
        for i in range(1, div_line_count+1):
            string_block.append([])

        # put string to the line they should be.
        cli = 0  # current line index
        while cli < len(string_block):
            for div_line in div_line_info:
                div_list = div_line['divs']
                for div in div_list:
                    cdli = 0  # current div line index
                    for string_line in div._renderer._get_string_list():
                        string_block[cli+cdli].append(string_line)
                        cdli += 1
                # go to the next line.
                cli += div_line['height']
        return string_block

    # def render(self) -> str:
    #     """
    #     by calling render, it will return a formatted string.
    #     """
    #     _item_to_print = ''
    #     self._content_layout()
    #     return _item_to_print
    #
    # def _content_layout(self):
    #     container_size = self.div_instance.size
    #     contents_list = self.get_contents_list()
    #     self._content_row_layout(container_size, contents_list)
    #
    # def _content_row_layout(self, container_size, contents_list):
    #     # check if
    #
    #     # content_lines: a list of content line.
    #     # a content_line contains content which are supposed to be aligned in one line.
    #     content_lines = []
    #     content_line = []
    #     line_width = container_size['width']
    #     # be careful that there's an "s".
    #     content_line_width = 0
    #     content_index = 0
    #
    #     while content_index <= len(contents_list):
    #         content = contents_list[content_index]
    #         content_line_width += content['width']
    #         if content_line_width > container_size['width']:
    #             content_line.append(content)
    #
    # def get_contents_list(self):
    #     contents_size = []
    #     for content in self.div_instance._container:
    #         height = content.get_size('height')
    #         width = content.get_size('width')
    #         contents_size.append({'div': content, 'name': content.name, 'height': height, 'width': width})
    #     return contents_size


