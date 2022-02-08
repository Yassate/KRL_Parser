from symbols import *


class ScopedSymbolTable:
    def __init__(self, name, lvl, enc_scope=None):
        self._symbols = {}
        self._childscopes = []
        self._inputs = self._outputs = None
        self.name = name
        self.lvl = lvl
        self.enc_scope = enc_scope
        self._init_builtins()
        if lvl == 0:
            self._init_inputs_outputs()
        if enc_scope:
            enc_scope.append_child(self)

    def _init_builtins(self):
        builtin_types = ["INT", "REAL", "BOOL", "CHAR", "E6POS", "E6AXIS"]
        for type_ in builtin_types:
            self.insert(BuiltInTypeSymbol(type_))

    def _init_inputs_outputs(self):
        self.insert(ArraySymbol(name="$IN", type_="BOOL", size=8196))
        self.insert(ArraySymbol(name="$OUT", type_="BOOL", size=8196))

    # def __str__(self):
    #     h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
    #     lines = ['\n', h1, '=' * len(h1)]
    #     for header_name, header_value in (
    #         ('Scope name', self.scope_name),
    #         ('Scope level', self.scope_level),
    #         ('Enclosing scope',
    #          self.enclosing_scope.scope_name if self.enclosing_scope else None)
    #     ):
    #         lines.append('%-15s: %s' % (header_name, header_value))
    #     h2 = 'Scope (Scoped symbol table) contents'
    #     lines.extend([h2, '-' * len(h2)])
    #     lines.extend(
    #         ('%7s: %r' % (key, value))
    #         for key, value in self._symbols.items()
    #     )
    #     lines.append('\n')
    #     s = '\n'.join(lines)
    #     return s

    def __repr__(self):
        enc_scope = self.enc_scope.name if self.enc_scope else "None"
        return f"Scope: {self.name}, level: {self.lvl}, enclosing scope: {enc_scope}"

    def insert(self, symbol):
        # print(f"Insert: {symbol.name}")
        self._symbols[symbol.name] = symbol

    # TODO >> Lookup should be case insensitive
    def lookup(self, name):
        #print(f"Lookup: {name}")
        if '[' in name and ']' in name:
            prefix = name.split('[')[0]
            index = name.split('[')[1][:-1]
            found = self._symbols.get(prefix)
            if isinstance(found, ArraySymbol):
                if found.size > index:
                    return found
        else:
            return self._symbols.get(name)

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
