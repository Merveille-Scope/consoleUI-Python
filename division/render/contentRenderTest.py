class TempDiv:
    _render_debug = False
    display = 'block'  # or 'float'

    container = []
    renderer = None

    def __init__(self):
        self._size = {'width': 30, 'height': 5}

    def get_raw_content(self, cursor="long_str"):
        string_dict = {'long_str': 'She dressed me with pantyhose and a pair of my panties '
                                   'in a pink lingerie and sat me on the side of the bed. '
                                   'I had a little more space than I would normally have '
                                   'for a girl and she had one knee up against the wall.',
                       'short_str': 'She dressed me with pantyhose and a pair of my panties',
                       'one_line_str': 'string in line.',
                       'chinese_str': '对我个人而言，人类之光连裤袜不仅仅是一个重大的事件，还可能会改变我的人生。'
                                      '就我个人来说, 人类之光连裤袜对我的意义, 不能不说非常重大. 本人也是经过了深思熟虑,在每个日日夜夜思考这个问题.'
                                      '克劳斯·莫瑟爵士在不经意间这样说过 : 教育需要花费钱，而无知也是一样。'
                                      '所谓人类之光连裤袜, 关键是人类之光连裤袜需要如何写. 洛克曾经提到过 : 学到很多东西的诀窍，就是一下子不要学很多。'
                                      '带着这句话, 我们还要更加慎重的审视这个问题: 我认为, 在这种困难的抉择下, 本人思来想去, 寝食难安.'
                                      '可是，即使是这样，人类之光连裤袜的出现仍然代表了一定的意义。 '
                       }
        return string_dict[cursor]

    def print_div(self):
        pass

    @property
    def size(self):
        return self._size


class Render:
    def __init__(self, div_instance: TempDiv, row_sep=' | ', line_sep=''):
        """
        :param div_instance: the div which initializes Render.
        :param row_sep: a pattern to separate two div in same line.
        :param line_sep: a pattern to separate div in next line.
        """
        self.div_instance = div_instance
        self.debug = self.div_instance._render_debug
        self._row_sep = row_sep
        self._line_sep = line_sep
        self.max_size = self.div_instance.size

    def render(self):
        return self.div_instance.print_div()

    @staticmethod
    def string_length(string):
        length = 0
        for char in string:
            length += ContentRender.character_width(char)
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


class ContentRender(Render):
    temp_raw_content_sel = 'long_str'

    def __init__(self, div_instance):
        super().__init__(div_instance)
        self.content = self.div_instance.get_raw_content(self.temp_raw_content_sel)  # information of string.
        self.content = self.content.replace("\n", " ").replace("\t", "    ")  # these invisible chars are not expected.

    def get_format_content(self):
        self.content = self.div_instance.get_raw_content(self.temp_raw_content_sel)
        string_lines = self._format_content_according_to_width()
        string_lines = self._format_content_according_to_height(string_lines)
        return string_lines

    def _format_content_according_to_width(self):
        char_lines = self._cut_string_in_char_lines()
        string_lines = []
        for char_line in char_lines:
            line = ''
            for char in char_line:
                line += char
            string_lines.append(line)
        return string_lines

    def _format_content_according_to_height(self, string_lines):
        div_height = self.max_size['height']
        total_lines = len(string_lines)
        if total_lines > div_height:
            string_lines = string_lines[:div_height - 1]
            folding_info = "%s more line(s) folded..." % (total_lines - div_height)
            if self.max_size['width'] >= self.string_length(folding_info):
                string_lines.append(folding_info)
            elif self.max_size['width'] >= 3:
                string_lines.append('...')
            else:
                string_lines.append('~')
        return string_lines

    def _cut_string_in_char_lines(self):
        max_line_width = self.max_size['width']
        total_length = self.string_length(self.content)

        char_list = list(self.content)
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


class ContainerRender(Render):
    def __init__(self, div_instance):
        super().__init__(div_instance)
        self.div_list = self.div_instance

    def get_format_content(self):
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
            if string_length < self.max_size['width']:
                string_block_list[line_index] += ' ' * (self.max_size['width'] - string_length)
            line_index += 1
        return string_block_list

    def _form_div_lines(self):
        container = self.div_instance.container
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
                    for string_line in div.renderer._get_string_list():
                        string_block[cli+cdli].append(string_line)
                        cdli += 1
                # go to the next line.
                cli += div_line['height']
        return string_block


# test for content render
d1 = TempDiv()
d1._size['width'] = 20
d1._size['height'] = 5
content_r = ContentRender(d1)
d1.render = content_r
fsl = d1.render.get_format_content()
print(d1)
for line in fsl:
    print(line)

d2 = TempDiv()
d2._size['width'] = 40
d2._size['height'] = 5
d2.render = ContentRender(d2)
d2.render.temp_raw_content_sel = 'chinese_str'
fsl = d2.render.get_format_content()
print(d2)
for line in fsl:
    print(line)

d3 = TempDiv()
d3.display = 'float'
d3._size['width'] = 20
d3._size['height'] = 5
d3.render = ContentRender(d3)
d3.render.temp_raw_content_sel = 'short_str'
fsl = d3.render.get_format_content()
print(d3)
for line in fsl:
    print(line)

d4 = TempDiv()
d4._size['width'] = 15
d4._size['height'] = 5
d4.render = ContentRender(d4)
d4.render.temp_raw_content_sel = 'one_line_str'
fsl = d4.render.get_format_content()
print(d4)
for line in fsl:
    print(line)


# test for container render
container_div = TempDiv()
container_div.container = [d1, d2, d3, d4]
container_r = ContainerRender(container_div)
container_div.renderer = container_r

string_block = container_div.renderer.get_format_content()
print(len(string_block))
for item in string_block:
    print(item)
line_block = container_div.renderer.get_format_string_block()
for line in line_block:
    print(line)

