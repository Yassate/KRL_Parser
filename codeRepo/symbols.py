class Symbol:
    def __init__(self, name):
        self.name = name.lower()

    def __str__(self):
        return f"{self.name}"


class VarSymbol(Symbol):
    def __init__(self, name, type_=None, typename=None):
        super().__init__(name)
        self.type_ = type_
        self.typename = typename

    def __str__(self):
        return f"{self.name}, type: {self.typename}"

    def fill_in_types_by_typename(self, symtable):
        self.type_ = symtable.lookup(self.typename)


class CallableSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)


class BuiltInTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)


class StructTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)
        self.members = {}

    def add_member(self, member):
        self.members[member.name] = member

    def fill_in_types_by_typename(self, symtable):
        for symbol in self.members.values():
            symbol.fill_in_types_by_typename(symtable)


class ArraySymbol(VarSymbol):
    def __init__(self, name, typename=None, size=0):
        super().__init__(name=name, typename=typename)
        self.size = size


class ProcedureSymbol(CallableSymbol):
    def __init__(self, name, ctx):
        super(ProcedureSymbol, self).__init__(name)
        self.ctx = ctx


class FunctionSymbol(CallableSymbol):
    def __init__(self, name, ctx, return_symbol):
        super(FunctionSymbol, self).__init__(name)
        self.ctx = ctx
        self.returnSymbol = return_symbol

    def fill_in_types_by_typename(self, symtable):
        self.returnSymbol.fill_in_types_by_typename(symtable)


class DatFileSymbol(CallableSymbol):
    def __init__(self, name, ctx):
        super(DatFileSymbol, self).__init__(name)
        self.ctx = ctx
        self.executed = False
