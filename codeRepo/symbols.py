

class TypeSymbol:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"


class VarSymbol:
    def __init__(self, name, type_=None, typename=None):
        self.name = name
        self.type_ = type_
        self.typename = typename

    def __str__(self):
        return f"{self.name}, type: {self.typename}"

    def fill_in_type_by_typename(self, symtable):
        self.type_ = symtable.lookup(self.typename)


class CallableSymbol():
    def __init__(self, name):
        self.name = name


class BuiltInTypeSymbol(TypeSymbol):
    def __init__(self, name):
        super().__init__(name)


class StructTypeSymbol(TypeSymbol):
    def __init__(self, name):
        super().__init__(name)
        self.members = []

    def add_member(self, member):
        self.members.insert(member)

    def fill_in_member_types_by_typename(self, symtable):
        for symbol in self.members:
            if isinstance(symbol, VarSymbol):
                symbol.type_ = symtable.lookup(symbol.typename)
            elif isinstance(symbol, StructTypeSymbol):
                symbol.fill_in_member_types_by_typename(self)


class ArraySymbol(VarSymbol):
    def __init__(self, name, typename=None, size=0):
        super().__init__(name=name, typename=typename)
        self.size = size


class ProcedureSymbol(CallableSymbol):
    def __init__(self, name, params=None, ctx=None):
        super(ProcedureSymbol, self).__init__(name)
        self.params = params if params is not None else []
        self.ctx = ctx


class SubroutineSymbol(CallableSymbol):
    def __init__(self, name, ctx=None):
        super(SubroutineSymbol, self).__init__(name)
        self.ctx = ctx
