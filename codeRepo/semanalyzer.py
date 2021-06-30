from krlVisitor import krlVisitor
from krlParser import krlParser
from symtables import *
import coloredlogs
import logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


class ScopeStack:
    def __init__(self):
        self._records = []
        global_scope = ScopedSymbolTable(scope_name="GLOBAL", scope_level=1)
        self.push(global_scope)

    def push(self, scope):
        self._records.append(scope)

    def pop(self):
        return self._records.pop()

    def peek(self):
        return self._records[-1]

    def peek_global(self):
        return self._records[0]

    def __str__(self):
        s = '; '.join(repr(ar) for ar in reversed(self._records))
        s = f'Scope stack, scopes inside: {s}'
        return s

    def __repr__(self):
        return self.__str__()


# TODO >> SEMANTIC ANALYZER TO COMPLETE REBUILD, SOME METHODS SHOULD BE TAKEN FROM krlInterpreter()
class SemanticAnalyzer(krlVisitor):
    def __init__(self, scope_stack):
        super().__init__()
        self._scope_stack = scope_stack

    @property
    def _current_symtable(self):
        return self._scope_stack.peek()

    @_current_symtable.setter
    def _current_symtable(self, new_cur_scope):
        self._scope_stack.push(new_cur_scope)

    def visitChild(self, ctx, index=0):
        return self.visit(ctx.getChild(index))

    def visitModuleData(self, ctx: krlParser.ModuleContext):
        module_name = self.visit(ctx.moduleName())
        logger.debug(f"Visiting module data {module_name}")
        global_scope = self._scope_stack.peek_global()
        global_scope.insert(ModuleSymbol(module_name, ctx))
        new_scope = ScopedSymbolTable(module_name, scope_level=2, enclosing_scope=global_scope)
        self._scope_stack.push(new_scope)
        return self.visitChildren(ctx)

    def visitEnumDefinition(self, ctx: krlParser.EnumDefinitionContext):
        pass

    def visitModuleName(self, ctx: krlParser.ModuleNameContext):
        return self.visit(ctx.IDENTIFIER())

    # TODO >> this method is copy of visitVariableDeclarationInDataList; to refactor
    def visitVariableDeclaration(self, ctx: krlParser.VariableDeclarationContext):
        if ctx.DECL() is not None:
            var_type = self.visit(ctx.typeVar())
            self._current_symtable.insert(Symbol(self.visit(ctx.variableName()), var_type))
            var_list_rest = ctx.variableListRest()
            if var_list_rest:
                for name in self.visit(var_list_rest):
                    self._current_symtable.insert(Symbol(name, var_type))

    def visitVariableDeclarationInDataList(self, ctx: krlParser.VariableDeclarationInDataListContext):
        if ctx.DECL():
            var_type = self.visit(ctx.typeVar())
            self._current_symtable.insert(Symbol(self.visit(ctx.variableName()), var_type))
            var_list_rest = ctx.variableListRest()
            if var_list_rest:
                for name in self.visit(var_list_rest):
                    self._current_symtable.insert(Symbol(name, var_type))
            # TODO >> implement GLOBAL/CONST declaration handling
        # TODO >> what to return?

    def visitVariableInitialisation(self, ctx: krlParser.VariableInitialisationContext):
        return self.visitChild(ctx, 1)

    def visitTerminal(self, node):
        return node.getText()

    def visitVariableListRest(self, ctx: krlParser.VariableListRestContext):
        names = []
        for name in ctx.variableName():
            names.append(self.visit(name))
        return names
