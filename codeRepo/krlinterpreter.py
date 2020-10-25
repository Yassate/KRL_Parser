from krlVisitor import krlVisitor
from krlLexer import krlLexer
from krlParser import krlParser
from symtables import *
from callstack import Callstack, ActivationRecord, ARType

# TODO >> IMPLEMENTATION IS COPIED FROM SEMANALYZER.PY -> TO CHANGE
class KrlInterpreter(krlVisitor):
    def __init__(self):
        super().__init__()
        self._callstack = Callstack()

    def _parse_literal(self, ctx):
        literal_type = ctx.getChild(0).symbol.type
        if literal_type == krlLexer.FLOATLITERAL:
            return float(ctx.getText())
        elif literal_type == krlLexer.INTLITERAL:
            return int(ctx.getText())
        elif literal_type == krlLexer.TRUE or literal_type == krlLexer.FALSE:
            return bool(ctx.getText())
        elif literal_type == krlLexer.CHARLITERAL or literal_type == krlLexer.STRINGLITERAL:
            return ctx.getText()

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

    def visitModuleName(self, ctx: krlParser.ModuleNameContext):
        scope_name = ctx.IDENTIFIER().accept(self)
        a_record = ActivationRecord(name=scope_name, type=ARType.MODULE, nesting_level=1)
        self._callstack.push(a_record)
        self.visitChildren(ctx)
        self._callstack.pop()
    # TODO I WAS HERE

    def visitVariableDeclaration(self, ctx: krlParser.VariableDeclarationContext):
        if ctx.DECL() is not None:
            var_type = ctx.typeVar().accept(self)
            self._currentscope.insert(Symbol(ctx.variableName().accept(self), var_type))
            var_list_rest = ctx.variableListRest()
            if var_list_rest is not None:
                for name in var_list_rest.accept(self):
                    self._currentscope.insert(Symbol(name, var_type))

    def visitVariableDeclarationInDataList(self, ctx: krlParser.VariableDeclarationInDataListContext):
        if ctx.DECL() is not None:
            var_type = ctx.typeVar().accept(self)
            self._currentscope.insert(Symbol(ctx.variableName().accept(self), var_type))
            var_list_rest = ctx.variableListRest()
            if var_list_rest is not None:
                for name in var_list_rest.accept(self):
                    self._currentscope.insert(Symbol(name, var_type))

    def visitVariableInitialisation(self, ctx: krlParser.VariableInitialisationContext):
        return ctx.getChild(1).accept(self)

    def visitLiteral(self, ctx: krlParser.LiteralContext):
        if isinstance(ctx.getChild(0), krlParser.StructLiteralContext):
            return self.visitChildren(ctx)
        elif isinstance(ctx.getChild(0), krlParser.EnumElementContext):
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


    # Those methods should be probably used in interpreter, not in semanalyzer
    def visitStructElementList(self, ctx: krlParser.StructElementListContext):
        struct_elements = {}
        for a in ctx.children:
            element = a.accept(self)
            if len(element) > 1:
                struct_elements.update(element)
        return struct_elements

    def visitStructElement(self, ctx: krlParser.StructElementContext):
        key = ctx.getChild(0).getText()
        val = ctx.getChild(1).accept(self)
        return {key: val}
