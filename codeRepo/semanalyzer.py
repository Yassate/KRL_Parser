from krlVisitor import krlVisitor
from krlParser import krlParser
from symtables import *


# TODO >> SEMANTIC ANALYZER TO COMPLETE REBUILD, SOME METHODS SHOULD BE TAKEN FROM krlInterpreter()
class SemanticAnalyzer(krlVisitor):
    def __init__(self, global_symtable=None, module_symtable=None, current_symtable=None):
        super().__init__()
        self._global_symtable = global_symtable
        self._module_symtable = module_symtable
        self._current_symtable = global_symtable

    def get_global_symtable(self):
        return self._global_symtable

    def get_module_symtable(self):
        return self._module_symtable

    def get_module_name(self):
        return self._module_symtable.scope_name

    def visitChild(self, ctx, index=0):
        return self.visit(ctx.getChild(index))

    def visitModuleData(self, ctx: krlParser.ModuleContext):
        module_name = self.visit(ctx.moduleName())
        self._current_symtable.insert(ModuleSymbol(module_name, ctx))
        self._module_symtable = ScopedSymbolTable(module_name, scope_level=2, enclosing_scope=self._current_symtable)
        self._current_symtable = self._module_symtable
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
