from krlVisitor import krlVisitor
from krlLexer import krlLexer
from krlParser import krlParser
from callstack import Callstack, ActivationRecord, ARType
from kuka_datatypes import E6Pos, E6Axis
from iksolver import CustomKukaIKSolver, dh_KR360_R2830
from icecream import ic


class variableFactory():
    def __init__(self):
        pass

    @staticmethod
    def get_variable(var_value, var_type):
        if var_type.upper() == "INT":
            return int(var_value)
        elif var_type.upper() == "E6POS":
            return E6Pos.from_krl_struct(var_value)
        else:
            return var_value


class KrlInterpreter(krlVisitor):
    def __init__(self, module_symtable):
        super().__init__()
        self._callstack = Callstack()
        self._module_symtable = module_symtable
        self._current_symtable = module_symtable
        self._var_factory = variableFactory()
        self.ik_solver = CustomKukaIKSolver(dh_KR360_R2830)

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
        scope_name = ctx.moduleName().accept(self)
        a_record = ActivationRecord(name=scope_name, type=ARType.MODULE, nesting_level=1, enclosing_ar=self._callstack.peek())
        self._callstack.push(a_record)
        self.visitChildren(ctx)

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
                ar.initialize_var(var_name=var_name, value=self._var_factory.get_variable(value, var_type))

            if var_list_rest is not None:
                for name in var_list_rest.accept(self):
                    pass
                    # TODO >> Implement multiple variable declaration (eg. DECL INT I,X,V = 0)

    def visitVariableInitialisation(self, ctx: krlParser.VariableInitialisationContext):
        return ctx.getChild(1).accept(self)

    def visitLiteral(self, ctx: krlParser.LiteralContext):
        if ctx.structLiteral() is not None or ctx.enumElement() is not None:
            return self.visitChildren(ctx)
        else:
            return self._parse_literal(ctx)

    def visitStructLiteral(self, ctx: krlParser.StructLiteralContext):
        return ctx.structElementList().accept(self)

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
        elif literal_type == krlLexer.CHARLITERAL or literal_type == krlLexer.STRINGLITERAL:
            return value

    def visitTerminal(self, node):
        return node.getText()

    def visitUnaryPlusMinuxExpression(self, ctx:krlParser.UnaryPlusMinuxExpressionContext):
        if len(ctx.children) > 1:
            return int(ctx.getChild(0).getText() + '1') * ctx.getChild(1).accept(self)
        else:
            return self.visitChildren(ctx)

    def visitPtpMove(self, ctx: krlParser.PtpMoveContext):
        target_name = self.visitChild(ctx, 1)
        target_e6pos = self._callstack.peek().get(target_name)
        print(f"Robot goes with PTP movement to: {target_name}")
        calc_axes = self.ik_solver.perform_ik(input_e6pos=target_e6pos, prev_e6_axis=E6Axis(axis_values=(0,0,0,0,0,0)))
        print(calc_axes)
        return self.visitChildren(ctx)

    def visitSubprogramCall(self, ctx:krlParser.SubprogramCallContext):
        if ctx.arguments() is not None:
            pass
            #print(ctx.arguments().accept(self))
            #print(ctx.arguments())
        return self.visitChildren(ctx)


    #TODO >> Multiple dimension arrays to be implemented
    def visitAssignmentExpression(self, ctx:krlParser.AssignmentExpressionContext):
        var_name, index = self.visitChild(ctx, 0)
        var_name_ctx =ctx.getChild(0)

        value = self.visitChild(ctx, 2)
        ar = self._callstack.peek()

        if index:
            ar[var_name][index] = value
            print(f"{var_name}[{index}] : {value}")
        else:
            ar[var_name] = value
            print(f"{var_name} = {value}")

    def visitVariableName(self, ctx:krlParser.VariableNameContext):
        var_name = ctx.IDENTIFIER().getText()
        index = ctx.arrayVariableSuffix()
        if index:
            index = index.accept(self)
        return var_name, index

    def visitArrayVariableSuffix(self, ctx:krlParser.ArrayVariableSuffixContext):
        return self.visitChild(ctx, 1)

    #def visitVariableListRest(self, ctx: krlParser.VariableListRestContext):
        #names = []
        #for name in ctx.variableName():
            #names.append(name.accept(self))
        #return names
