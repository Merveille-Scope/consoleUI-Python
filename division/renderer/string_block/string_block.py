# implement of StringBlock

# StringBlock is trying to solve the problem of formatting string into a "block".
# it will cut a long string in lines so that the string will be shown in a rectangle.


class StringBlock:
    _trim = True
    _folding_message = 'lines folded...'

    def __init__(self, height: int, width: int, **block_styles):
        """
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
        self._string_content = ''
        self._height = height
        self._width = width

        self.set_block_styles(**block_styles)
    
    def set_block_styles(self, **block_styles):
        if block_styles:
            self._trim = True if 'trim' not in block_styles else block_styles['trim']
            self._h_trim = block_styles.get('h_trim')
            self._w_trim = block_styles.get('w_trim')
            self._set_size(**block_styles)
            self._folding_message = block_styles['folding_message'] if block_styles.get('folding_message') else 'lines folded...'
        else:
            self._trim = True if 'trim' not in block_styles else block_styles['trim']
            self._h_trim = None
            self._w_trim = None
            self._set_size(height=self._height, width=self._width)
    
    def _set_size(self, **size):
        """
        height: height in line.
        width: width in mono-spaced character.
        """
        if 'height' in size:
            self._height = size['height']
        if 'width' in size:
            self._width = size['width']
    
    def set_string_content(self, string_content):
        string_content = string_content.replace('\t', '    ').replace('\n', ' ')
        # replace: invisible character must have constant length.
        self._string_content = string_content
    
    def _form_raw_string_list(self):
        """
        it will simply convert string into string list with no trimming or any formatting.
        """

        # TODO: extract a generator method to form a string line from current method.
        # TODO: maybe someday, English words would be aggregates separated by ' '.

        character_list = list(self._string_content)
        current_line = []
        string_list = []

        for character in character_list:
            # if next character will make current line become too long.
            if (StringBlock._char_list_length(current_line) + StringBlock.character_width(character)) > self._width:
                # save it to the next line's first character.
                next_lines_first_character = character
                # append current str(line) to string line.
                string_list.append("".join(current_line))
                # move current line to the next line and put next line's first character in it.
                current_line = [next_lines_first_character]
                # reset next line's first character to None.
                next_lines_first_character = None
            else:
                current_line.append(character)
        else:
            # finally, for the last line.
            if current_line:
                string_list.append("".join(current_line))

        return string_list
    
    def _form_format_string_list(self):
        """
        it will make sure everyline appears in same length by filling blank(' ') to line shorter than width.
        """
        raw_string_list = self.raw_string_list
        format_string_list = []
        for string in raw_string_list:
            line_length = StringBlock.string_length(string)
            string += ' ' * (self._width - line_length)
            format_string_list.append(string)
        return format_string_list

    def _form_format_string(self):
        string_list = self.format_string_list
        return "\n".join(string_list)
    
    def _form_trimmed_format_string(self):
        string_list = self.format_string_list_trimmed
        return "\n".join(string_list)
    
    def _trim_string_list(self, string_list):
        if not self._h_trim:
            return self._basic_h_trim(string_list)
        # else, some special trim method.
        if not self._w_trim:
            # this method is not useful, suppressed.
            return self._basic_w_trim(string_list)
        # else, some special trim method.
    
    def _basic_h_trim(self, string_list):
        # TODO: trim by height
        string_height = len(string_list)
        if string_height > self._height:
            string_list = list(string_list[:self._height - 1])  # since it's a tuple
            folding_message = str(string_height - self._height - 1) + self._folding_message
            if StringBlock.string_length(folding_message) > self._width:
                folding_message = folding_message[:self._width]
            elif StringBlock.string_length(folding_message) < self._width:
                folding_message += ' ' * (self._width - StringBlock.string_length(folding_message))
            string_list.append(folding_message)
        return string_list

    def _basic_w_trim(self, string_list):
        # TODO: trim by width
        # need to consider how this method works.
        # because trimming string by width has already trimmed the string.
        return string_list

    @property
    def format_string_no_trim(self) -> str:  # test passed.
        """
        you can get formatted string without trimming.
        """
        return self._form_format_string()
    
    @property
    def format_string_trimmed(self) -> str:
        return self._form_trimmed_format_string()

    @property
    def format_string_block(self):
        """
        you can set StringBlock.default_trim to *True* (default) to make format_string always return trimmed string block.

        or you can change it to *False* to make format_string always return string block without trimming.
        """
        if self._trim:
            return self._form_trimmed_format_string()
        else:
            return self._form_format_string()

    @property
    def format_string_list(self) -> tuple:  # test passed.
        """
        you can get a list of string that fills all blanks in a div has indicated height and width.
        """
        if self._trim:
            return tuple(self.format_string_list_trimmed)
        else:
            return tuple(self.format_string_list_no_trim)

    @property
    def raw_string_list(self) -> tuple:  # test passed.
        """
        you can get a list of string that is able to fit into the indicated height and width.
        """
        return tuple(self._form_raw_string_list())
    
    @property
    def format_string_list_no_trim(self):
        return tuple(self._form_format_string_list())
    
    @property
    def format_string_list_trimmed(self):
        return self._trim_string_list(self._form_format_string_list())
    
    @property
    def raw_string(self) -> str:  # test passed
        """
        simply get the raw string, which is what you put in.
        """
        return self._string_content
    
    @staticmethod
    def string_length(string):
        return StringBlock._char_list_length(list(string))

    @staticmethod
    def _char_list_length(character_list: list) -> int:
        length = 0
        for char in character_list:
            length += StringBlock.character_width(char)
        return length

    @staticmethod
    def character_width(character):
        """
        only considering ASCII characters, please don't make strange things in it.
        """
        inside_code = ord(character)
        if inside_code > 255:
            chara_width = 2
        # still a problem: what if \t in the cell context?
        # update: the content string has .replace() "\n" and "\t" into " " and "    ".
        else:
            chara_width = 1
        return chara_width


if __name__ == "__main__":
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
    string_block = StringBlock(10, 40)
    string_block.set_string_content(string)
    for line in string_block.format_string_list:
        print(line)

