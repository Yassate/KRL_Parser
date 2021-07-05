

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


class TypeSymbol:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )


class BuiltInTypeSymbol(TypeSymbol):
    def __init__(self, name):
        super().__init__(name)


class CallableSymbol():
    def __init__(self, name):
        self.name = name


class StructTypeSymbol(TypeSymbol):
    def __init__(self, name):
        super().__init__(name)
        self.members = []

    def add_member(self, member):
        self.members.insert(member)

    def fill_in_member_types_by_typename(self, symtable):
        for symbol in self.members:
            if isinstance(symbol, Symbol):
                symbol.type_ = symtable.lookup(symbol.typename)
            elif isinstance(symbol, StructTypeSymbol):
                symbol.fill_in_member_types_by_typename(self)


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


class ProcedureSymbol(CallableSymbol):
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


class SubroutineSymbol(CallableSymbol):
    def __init__(self, name, ctx=None):
        super(SubroutineSymbol, self).__init__(name)
        self.ctx = ctx

    def __str__(self):
        return '<{class_name}(name={name})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
        )

    __repr__ = __str__
