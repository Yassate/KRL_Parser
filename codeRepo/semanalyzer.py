from krlVisitor import krlVisitor
from krlLexer import krlLexer
from krlParser import krlParser
from symtables import *
from dataclasses import dataclass


@dataclass
class E6Pos():
    X: float
    Y: float
    Z: float
    A: float
    B: float
    C: float
    S: int
    T: int
    A1: float
    A2: float
    A3: float
    A4: float
    A5: float
    A6: float
    E1: float
    E2: float
    E3: float
    E4: float
    E5: float
    E6: float


# TODO: #OVERALL >> Implement 2 visitors - first for Semantic Analysis ang getting definitions, second for evaluate
class SemanticAnalyzer(krlVisitor):
    def __init__(self):
        super().__init__()
        self._globalscope = ScopedSymbolTable(scope_name="GLOBAL", scope_level=1)
        self._modulescope = None
        self._currentscope = None


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
        if self._modulescope is None:
            self._modulescope = ScopedSymbolTable(scope_name, scope_level=2)
            self._currentscope = self._modulescope
        return self.visitChildren(ctx)

    def visitDataList(self, ctx: krlParser.DataListContext):
        return self.visitChildren(ctx)

    # TODO >> this method is copy of visitVariableDeclarationInDataList; to refactor
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
            # TODO >> implement incorrect declaration handling (without "DECL"; maybe use code from assignment visitor"
        # TODO >> what to return?
        #return self.visitChildren(ctx)

    def visitVariableInitialisation(self, ctx: krlParser.VariableInitialisationContext):
        return ctx.getChild(1).accept(self)

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

    def visitLiteral(self, ctx: krlParser.LiteralContext):
        if isinstance(ctx.getChild(0), krlParser.StructLiteralContext):
            x = self.visitChildren(ctx)
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
