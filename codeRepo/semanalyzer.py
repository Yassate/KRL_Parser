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

    def get_global_symtable(self):
        return self._scope_stack.peek_global()

    def visitChild(self, ctx, index=0):
        return self.visit(ctx.getChild(index))

    #TODO >> Need to find other way for transfering symbol table between correct .dat and .src files"
    def visitModuleData(self, ctx: krlParser.ModuleContext):
        module_name = self.visit(ctx.moduleName()).lower()
        logger.debug(f"Visiting module data {module_name}")
        global_scope = self._scope_stack.peek_global()
        if self._current_symtable != global_scope:
            self._scope_stack.pop()
        global_scope.insert(SubroutineSymbol(module_name, ctx))
        if module_name != "config":
            new_scope = ScopedSymbolTable(module_name, scope_level=2, enclosing_scope=global_scope)
            self._scope_stack.push(new_scope)
        return self.visitChildren(ctx)

    def visitModuleRoutines(self, ctx: krlParser.ModuleRoutinesContext):
        ctx.symtable = self._current_symtable
        return self.visitChildren(ctx)

    def visitEnumDefinition(self, ctx: krlParser.EnumDefinitionContext):
        pass

    def visitStructureDefinition(self, ctx: krlParser.StructureDefinitionContext):
        typename = self.visit(ctx.typeName())
        symtable = self.get_global_symtable() if ctx.GLOBAL() else self._current_symtable
        struct_symbol = StructTypeSymbol(typename)

        for i, typeVarCtx in enumerate(ctx.typeVar()):
            members_type = self.visit(typeVarCtx)
            members_names = [self.visit(ctx.variableName(i))]
            members_names.extend(self.visit(ctx.variableListRest(i)))
            for member_name in members_names:
                struct_symbol.add_member(VarSymbol(member_name, typename=members_type))

        symtable.insert(struct_symbol)
        return self.visitChildren(ctx)

    def visitModuleName(self, ctx: krlParser.ModuleNameContext):
        return self.visit(ctx.IDENTIFIER())

    def visitVariableDeclarationInDataList(self, ctx: krlParser.VariableDeclarationInDataListContext):
        if ctx.DECL():
            var_typename = self.visit(ctx.typeVar())
            var_name = self.visit(ctx.variableName())
            symtable = self.get_global_symtable() if ctx.GLOBAL() else self._current_symtable
            symtable.insert(VarSymbol(name=var_name, typename=var_typename))
            var_list_rest = ctx.variableListRest()
            if var_list_rest:
                for var_name in self.visit(var_list_rest):
                    symtable.insert(VarSymbol(name=var_name, typename=var_typename))

    def visitVariableInitialisation(self, ctx: krlParser.VariableInitialisationContext):
        return self.visitChild(ctx, 1)

    def visitTerminal(self, node):
        return node.getText()

    def visitVariableListRest(self, ctx: krlParser.VariableListRestContext):
        names = []
        for name in ctx.variableName():
            names.append(self.visit(name))
        return names

    # TODO >> Indexed variables handling, for now - skipped
    def visitVariableName(self, ctx: krlParser.VariableNameContext):
        var_name = ctx.IDENTIFIER().getText()
        var_suffix = ctx.arrayVariableSuffix()
        indices = self.visit(var_suffix) if var_suffix else ''
        return var_name + indices

    def visitArrayVariableSuffix(self, ctx: krlParser.ArrayVariableSuffixContext):
        indices = []
        for i in range(len(ctx.children)):
            indices.append(self.visitChild(ctx, i))
        return ''.join(map(str, indices))
        return ''
