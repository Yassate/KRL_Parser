from krlVisitor import krlVisitor
from krlLexer import krlLexer
from krlParser import krlParser
from symtables import *
from callstack import Callstack, ActivationRecord, ARType

# TODO >> IMPLEMENTATION IS COPIED FROM SEMANALYZER.PY -> TO CHANGE
class KrlInterpreter(krlVisitor):
    def __init__(self, module_symtable):
        super().__init__()
        self._callstack = Callstack()
        self._module_symtable = module_symtable
        self._current_symtable = module_symtable

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

    def visitModuleData(self, ctx:krlParser.ModuleDataContext):
        scope_name = ctx.moduleName().accept(self)
        a_record = ActivationRecord(name=scope_name, type=ARType.MODULE, nesting_level=1)
        self._callstack.push(a_record)
        self.visitChildren(ctx)
        self._callstack.pop()
        #TODO Callstack pop trzeba wywalic dopóki plik .src nie zostanie przemielony

    def visitModuleName(self, ctx: krlParser.ModuleNameContext):
        return ctx.IDENTIFIER().accept(self)


    #def visitVariableDeclaration(self, ctx: krlParser.VariableDeclarationContext):
        #if ctx.DECL() is not None:
            #var_type = ctx.typeVar().accept(self)
            #self._currentscope.insert(Symbol(ctx.variableName().accept(self), var_type))
            #var_list_rest = ctx.variableListRest()
            #if var_list_rest is not None:
                #for name in var_list_rest.accept(self):
                    #self._currentscope.insert(Symbol(name, var_type))

    def visitVariableDeclarationInDataList(self, ctx: krlParser.VariableDeclarationInDataListContext):
        if ctx.DECL() is not None:
            var_type = ctx.typeVar().accept(self)
            var_name = ctx.variableName().accept(self)
            var_list_rest = ctx.variableListRest()
            ar = self._callstack.peek()
            if ctx.variableInitialisation() is not None:
                value = ctx.variableInitialisation().accept(self)
                # TODO >> Value validation need to be added - checking type in symbol table?
                ar[var_name] = value
            if var_list_rest is not None:
                for name in var_list_rest.accept(self):
                    pass
                    # TODO >> implement multiple variable declaration (np. DECL INT I,X,V = 0)

    def visitVariableInitialisation(self, ctx: krlParser.VariableInitialisationContext):
        return ctx.getChild(1).accept(self)

    def visitStructElementList(self, ctx: krlParser.StructElementListContext):
        struct_elements = {}
        for struct_elem in ctx.structElement():
            element = struct_elem.accept(self)
            struct_elements.update(element)
        return struct_elements

    def visitStructElement(self, ctx: krlParser.StructElementContext):
        key = ctx.getChild(0).getText()
        val = ctx.getChild(1).accept(self)
        return {key: val}

    def visitLiteral(self, ctx: krlParser.LiteralContext):
        if ctx.structLiteral() is not None or ctx.enumElement() is not None:
            return self.visitChildren(ctx)
        else:
            return self._parse_literal(ctx)

    def visitStructLiteral(self, ctx: krlParser.StructLiteralContext):
        return ctx.structElementList().accept(self)

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

    def visitTerminal(self, node):
        return node.getText()

    #def visitVariableListRest(self, ctx: krlParser.VariableListRestContext):
        #names = []
        #for name in ctx.variableName():
            #names.append(name.accept(self))
        #return names
