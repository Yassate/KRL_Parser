from krlVisitor import krlVisitor
from krlLexer import krlLexer
from krlParser import krlParser
from callstack import ActivationRecord, ARType
from kuka_datatypes import E6Pos, E6Axis
import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

class VariableFactory():
    def __init__(self):
        self.structures_definitions = {
            ('X', 'Y', 'Z', 'A', 'B', 'C', 'S', 'T', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6'): "E6POS",
            ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6'): "E6AXIS"}

    @staticmethod
    def get_variable(var_value, var_type):
        var_type_capital = var_type.upper() if var_type else None
        if var_type_capital == "E6POS":
            return E6Pos.from_krl_struct(var_value)
        else:
            return var_value

    def get_var_type_by_struct_members(self, struct_members: tuple):
        if struct_members in self.structures_definitions.keys():
            return self.structures_definitions[struct_members]

    def get_var_by_discover(self, krl_struct: dict):
        keys = tuple(krl_struct.keys())
        var_type = self.get_var_type_by_struct_members(keys)
        return self.get_variable(krl_struct, var_type)


class KrlInterpreter(krlVisitor):
    def __init__(self, symtable=None, callstack=None, var_factory=None, ik_solver=None):
        super().__init__()
        self._callstack = callstack
        self._module_symtable = symtable
        self._current_symtable = symtable
        self._var_factory = var_factory
        self.ik_solver = ik_solver

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

    def visitTerminal(self, node):
        return node.getText()

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

    def visitModuleName(self, ctx: krlParser.ModuleNameContext):
        return ctx.IDENTIFIER().accept(self)

    def visitVariableInitialisation(self, ctx: krlParser.VariableInitialisationContext):
        return ctx.getChild(1).accept(self)

    def visitSubprogramCall(self, ctx: krlParser.SubprogramCallContext):
        return self.visitChildren(ctx)

    # TODO >> this method should find out what type of structure is that and return concrete object (eg. E6POS/AXIS)
    def visitStructLiteral(self, ctx: krlParser.StructLiteralContext):
        krl_struct: dict = ctx.structElementList().accept(self)
        return self._var_factory.get_var_by_discover(krl_struct)

    def visitModuleData(self, ctx: krlParser.ModuleDataContext):
        scope_name = ctx.moduleName().accept(self)
        a_record = ActivationRecord(name=scope_name, type_=ARType.MODULE, nesting_level=1, enclosing_ar=self._callstack.peek())
        self._callstack.push(a_record)
        self.visitChildren(ctx)


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
            var_name = ctx.variableName().accept(self).name
            var_list_rest = ctx.variableListRest()
            ar = self._callstack.peek()
            if ctx.variableInitialisation() is not None:
                value = ctx.variableInitialisation().accept(self)
                ar.initialize_var(var_name, value)

            #if var_list_rest is not None:
                #for name in var_list_rest.accept(self):
                    #pass

    def visitLiteral(self, ctx: krlParser.LiteralContext):
        if ctx.structLiteral() is not None or ctx.enumElement() is not None:
            return self.visitChildren(ctx)
        else:
            return self._parse_literal(ctx)

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


    #METHODS UNDER ARE COVERED WITH UNITTESTS
    def visitUnaryPlusMinuxExpression(self, ctx:krlParser.UnaryPlusMinuxExpressionContext):
        if ctx.primary():
            return self.visitChildren(ctx)
        else:
            return int(ctx.getChild(0).accept(self) + '1') * ctx.getChild(1).accept(self)

    def visitPtpMove(self, ctx: krlParser.PtpMoveContext):
        # TODO >> C_DIS/C_PTP should be checked (usually third child in ctx)
        target_e6pos = ctx.geometricExpression().accept(self)
        logger.debug(f"Robot goes with PTP movement to: {target_e6pos}")
        calc_axes = self.ik_solver.perform_ik(target_e6pos, prev_e6_axis=E6Axis(axis_values=(0, 0, 0, 0, 0, 0)))
        ar = self._callstack.peek()
        ar["$POS_ACT"] = target_e6pos
        ar["$AXIS_ACT"] = calc_axes
        logger.debug(calc_axes)

    def visitAssignmentExpression(self, ctx:krlParser.AssignmentExpressionContext):
        var_name = ctx.leftHandSide().accept(self)
        value = ctx.expression()[0].accept(self)
        indices = var_name.indices
        ar = self._callstack.peek()

        nextList = ar[var_name.name]
        if var_name.is_indexed():
            indices_count = len(indices)
            for i in range(0, indices_count - 1):
                nextList = nextList[indices[i]]
            nextList[indices[indices_count - 1]] = value
        else:
            ar[var_name.name] = value

    # TODO >> WRONGLY SETTED RESPONSIBILITIES -> ACTIVATION RECORD SHOULD RESOLVE IF IT'S ARRAY VARIABLE TYPE OR NOT/
    #we should ask only for name as string -> $IN[25] -> activation record resolves wherea and how it stores variable
    def visitVariableCall(self, ctx:krlParser.VariableCallContext):
        value = [
            lambda indices: ar[var_name.name],
            lambda indices: ar[var_name.name][indices[0]],
            lambda indices: ar[var_name.name][indices[0]][indices[1]],
            lambda indices: ar[var_name.name][indices[0]][indices[1]][indices[2]]]
        ar = self._callstack.peek()
        var_name = ctx.variableName().accept(self)
        indices_count = len(var_name.indices) if var_name.is_indexed() else 0

        return value[indices_count](var_name.indices)

    def visitVariableName(self, ctx:krlParser.VariableNameContext):
        var_name = ctx.IDENTIFIER().getText()
        indices = ctx.arrayVariableSuffix()
        indices = indices.accept(self) if indices else ''
        return var_name + indices

    def visitArrayVariableSuffix(self, ctx:krlParser.ArrayVariableSuffixContext):
        indices = []
        for i in range(len(ctx.children)):
            indices.append(self.visitChild(ctx, i))
        return ''.join(map(str, indices))


class VariableName:
    def __init__(self, name, indices=None):
        self.name = name
        self.indices = indices

    def is_indexed(self):
        return self.indices is not None

