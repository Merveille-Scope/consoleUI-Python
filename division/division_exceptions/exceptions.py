class DivisionError:
    def __init__(self, div):
        self.value = "DivisionError: %s" % div.get_div_name()

    def __str__(self):
        return self.value


class TooManyDivisionsError(DivisionError):
    def __init__(self, max_div):
        self.value = "No more than %s divisions shall be inited." % max_div


class NotContainerError(DivisionError):
    def __init__(self, div):
        self.value = "%s can't be a container. No Division shall be registered into it." % div.get_div_name()


class ContainerError(DivisionError):
    def __init__(self, div):
        self.value = "%s is a container. Only Division shall be registered into it." % div.get_div_name()


class RootDivisionError(DivisionError):
    def __init__(self, div):
        self.value = "%s is RootDivision. No parent div should be set." % div.get_div_name()


class NoParentDivisionError(DivisionError):
    def __init__(self, div):
        self.value = "%s must have a parent division." % div.get_div_name()


class ParentDivisionError(DivisionError):
    def __init__(self, div):
        self.value = "%s already has a parent division." % div.get_div_name()


class CallbackFunctionError(DivisionError):
    def __init__(self, div, callback):
        self.value = "%s: callback <%s> is not expected." % (div.get_div_name(), callback)


class NoCallbackAvailableError(CallbackFunctionError):
    def __init__(self, div, callback):
        self.value = "%s: no available callback found. callback=%s" % (div.get_div_name(), callback)


class DivisionOverflowError(DivisionError):
    def __init__(self, container, *child_div_list):
        self.value = "division overflow: %s" % container


class TableDivisionError(DivisionError):
    pass


class SeparatorError(TableDivisionError):
    def __init__(self, div):
        self.value = "%s: no separator \"%s\" shall be registered in a TableCell." % \
                     (div.get_div_name(), div.cell_separator)
