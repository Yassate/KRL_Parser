from krlVisitor import krlVisitor
from krlLexer import krlLexer
from krlParser import krlParser
from symtables import *


class SemanticAnalyzer(krlVisitor):
    def __init__(self):
        super().__init__()
        self._global_symtable = ScopedSymbolTable(scope_name="GLOBAL", scope_level=1)
        self._module_symtable = None
        self._current_symtable = None

    def get_global_symtable(self):
        return self._global_symtable

    def get_module_symtable(self):
        return self._module_symtable

    def get_module_name(self):
        return self._module_symtable.scope_name


    def _parse_literal(self, ctx):
        literal_type = ctx.getChild(0).symbol.type
        value = ctx.getText()
        if literal_type == krlLexer.FLOATLITERAL:
            return float(value)
        elif literal_type == krlLexer.INTLITERAL:
            return int(value)
        elif literal_type == krlLexer.TRUE or literal_type == krlLexer.FALSE:
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
        elif literal_type == krlLexer.CHARLITERAL:
            return value.strip("'")
        elif literal_type == krlLexer.STRINGLITERAL:
            return value.strip('"')


    def visitChildren(self, node):
        result = self.defaultResult()
        n = node.getChildCount()
        for i in range(n):
            if not self.shouldVisitNextChild(node, result):
                return result
            c = node.getChild(i)
            childResult = c.accept(self)
            if childResult is not None:
                result = childResult
        return result

    def visitChild(self, ctx, index):
        return ctx.getChild(index).accept(self)

    def visitModule(self, ctx: krlParser.ModuleContext):
        return self.visitChildren(ctx)

    def visitModuleData(self, ctx: krlParser.ModuleDataContext):
        return self.visitChildren(ctx)

    # TODO >> How to test it?
    def visitModuleName(self, ctx: krlParser.ModuleNameContext):
        scope_name = ctx.IDENTIFIER().accept(self)
        if self._module_symtable is None:
            self._module_symtable = ScopedSymbolTable(scope_name, scope_level=2)
            self._current_symtable = self._module_symtable

    # TODO >> this method is copy of visitVariableDeclarationInDataList; to refactor
    def visitVariableDeclaration(self, ctx: krlParser.VariableDeclarationContext):
        if ctx.DECL() is not None:
            var_type = ctx.typeVar().accept(self)
            self._current_symtable.insert(Symbol(ctx.variableName().accept(self), var_type))
            var_list_rest = ctx.variableListRest()
            if var_list_rest is not None:
                for name in var_list_rest.accept(self):
                    self._current_symtable.insert(Symbol(name, var_type))

    def visitVariableDeclarationInDataList(self, ctx: krlParser.VariableDeclarationInDataListContext):
        if ctx.DECL() is not None:
            var_type = ctx.typeVar().accept(self)
            self._current_symtable.insert(Symbol(ctx.variableName().accept(self), var_type))
            var_list_rest = ctx.variableListRest()
            if var_list_rest is not None:
                for name in var_list_rest.accept(self):
                    self._current_symtable.insert(Symbol(name, var_type))
            # TODO >> implement GLOBAL/CONST declaration handling
        # TODO >> what to return?
        #return self.visitChildren(ctx)

    def visitVariableInitialisation(self, ctx: krlParser.VariableInitialisationContext):
        return ctx.getChild(1).accept(self)

    def visitLiteral(self, ctx: krlParser.LiteralContext):
        if ctx.structLiteral() is not None or ctx.enumElement() is not None:
            return self.visitChildren(ctx)
        else:
            return self._parse_literal(ctx)

    def visitTerminal(self, node):
        return node.getText()

    def visitVariableListRest(self, ctx: krlParser.VariableListRestContext):
        names = []
        for name in ctx.variableName():
            names.append(name.accept(self))
        return names




