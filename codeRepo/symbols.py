# copyright RuslanSpivak.com


class Symbol:
    def __init__(self, name, type_=None, typename=None):
        self.name = name
        self.type_ = type_
        self.typename = typename

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )


class BuiltInTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)


class ArraySymbol(Symbol):
    def __init__(self, name, type_=None, size=0):
        super().__init__(name=name, type_=type_)
        self.size = size

    def __repr__(self):
        return "<{class_name}(name='{name}')(size='{size})'>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            size=self.size
        )


class StructSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)
        self.members = None


class ProcedureSymbol(Symbol):
    def __init__(self, name, params=None, ctx=None):
        super(ProcedureSymbol, self).__init__(name)
        self.params = params if params is not None else []
        self.ctx = ctx

    def __str__(self):
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.params,
        )

    __repr__ = __str__


class SubroutineSymbol(Symbol):
    def __init__(self, name, ctx=None):
        super(SubroutineSymbol, self).__init__(name)
        self.ctx = ctx

    def __str__(self):
        return '<{class_name}(name={name})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
        )

    __repr__ = __str__
