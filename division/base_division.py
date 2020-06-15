# impolement of division

# Division is handling the relationship among other divs.
# for example, which Division is in another Division.
# the 
#


import division.renderer


class BaseDivision:
    pass


class Division(BaseDivision):
    """
    a division can have other division in it by .register(other_div)
    """
    _div_count = 0
    _div_type = 'Division'

    @staticmethod
    def div_count():
        return Division._div_count

    def __init__(self, height: int, width: int, parent_division=None, **div_style):
        """
        params:
        height: height in line.
        width: width in mono-spaced character.

        optional params:
        parent_div: parent division, notice that some kinds of Divisions don't accept to be children.
        
        display: 'block' by default, if set 'float', it tries to be print at same line of the division before it.
        """
        Division._div_count += 1

        self._parent_div = parent_division

        self._set_div_name()

        self._renderer = None

        self._div_styles = div_style
        self._div_height = height
        self._div_width = width
    
    ################
    # div relationships
    ################
    def _set_div_name(self):
        # set id first.
        self.set_div_id()

        name = ''
        name += self._div_type + "<%s>" % self._div_id
        self._div_name = name
    
    def set_div_id(self):
        # knowing the recursive depth should be first.
        self.calculate_recursive_depth()

        # here is where causes the division count limitation.
        # if div_count over 999, the first digit couldn't express the recursive depth of the division.
        self._div_id = str(self.recursive_depth) + '_' + str(Division._div_count)

    def calculate_recursive_depth(self):
        if self._parent_div:
            self._recursive_depth = self._parent_div.recursive_depth + 1
        else:
            self._recursive_depth = 0
    
    ################
    # content
    ################
    def register(self, obj):
        """
        will be implemented respectively in ContentDivision and ContainerDivision.
        """
        ...

    ################
    # division styles
    ################
    def get_width(self):
        return self._div_width

    def get_height(self):
        return self._div_height

    def get_size(self):
        return {'height': self._div_height, 'width': self._div_width}

    def get_div_style(self):
        return self._div_styles

    ################
    # properties
    ################
    @property
    def recursive_depth(self):
        return self._recursive_depth

    @property
    def size(self):
        return self.get_size()

    @property
    def styles(self):
        return self.get_div_style()

    def __str__(self):
        return self._div_name

    ################
    # API
    ################

