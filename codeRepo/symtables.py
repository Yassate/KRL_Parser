from symbols import *


class ScopedSymbolTable:
    def __init__(self, name, enc_scope=None):
        self.name = name
        self.enc_scope = enc_scope
        self._symbols = {}
        self._childscopes = []
        self._init_builtins()
        if enc_scope:
            self.lvl = enc_scope.lvl+1
            enc_scope.append_child(self)
        else:
            self.lvl = 1
            self._init_inputs_outputs()

    def _init_builtins(self):
        builtin_types = ["int", "real", "bool", "char", "e6pos", "e6axis"]
        for type_ in builtin_types:
            self.insert(BuiltInTypeSymbol(type_))

    def _init_inputs_outputs(self):
        self.insert(ArraySymbol(name="$in", typename="bool", size=8196))
        self.insert(ArraySymbol(name="$out", typename="bool", size=8196))

    def __repr__(self):
        enc_scope = self.enc_scope.name if self.enc_scope else "None"
        return f"Scope: {self.name}, level: {self.lvl}, enclosing scope: {enc_scope}"

    def insert(self, symbol):
        # print(f"Insert: {symbol.name}")
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        name = name.lower()
        #print(f"Lookup: {name}")
        if '[' in name and ']' in name:
            prefix = name.split('[')[0]
            index = name.split('[')[1][:-1]
            found = self._symbols.get(prefix)
            if not (isinstance(found, ArraySymbol) and found.size > index):
                found = None
        else:
            found = self._symbols.get(name)
        if not found and self.lvl != 1:
            return self.enc_scope.lookup(name)
        else:
            return found

    def get_input(self, input_no):
        return self._inputs[input_no]

    def set_input(self, input_no, value):
        self._inputs[input_no] = bool(value)

    def get_output(self, output_no):
        return self._outputs[output_no]

    def set_output(self, output_no, value):
        self._outputs[output_no] = bool(value)

    def append_child(self, child_symtable):
        self._childscopes.append(child_symtable)

    def fill_in_types_by_typename(self):
        for symbol in self._symbols.values():
            # TODO >> Maybe it should be reworked? ABCs, filter or separate symtables for different symbol types
            if isinstance(symbol, (StructTypeSymbol, VarSymbol, FunctionSymbol)):
                symbol.fill_in_types_by_typename(self)
        for symtable in self._childscopes:
            symtable.fill_in_types_by_typename()
