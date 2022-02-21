from krlVisitor import krlVisitor
from krlLexer import krlLexer
from krlParser import krlParser
from callstack import ActivationRecord, ARType
from kuka_datatypes import E6Pos, E6Axis, KrlEnum
import coloredlogs
import logging

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


class VariableFactory:
    def __init__(self):
        self.structs_def = {
            ('X', 'Y', 'Z', 'A', 'B', 'C', 'S', 'T', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6'): "E6POS",
            ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6'): "E6AXIS"}

    def get_var_by_type(self, var_value, var_type):
        var_type_capital = var_type.upper() if var_type else None
        if var_type_capital == "E6POS":
            return E6Pos.from_krl_struct(var_value)
        else:
            return var_value

    def _get_var_type_by_struct_members(self, struct_members: tuple):
        struct_type = self.structs_def[struct_members] if struct_members in self.structs_def.keys() else "USER_DEFINED"
        return struct_type

    # INFO >> should be only used for creating object (E6POS/E6AXIS..) if PTP/LIN called on struct: PTP {X 1.0, Y 30...
    def get_var_by_discover(self, krl_struct: dict):
        keys = tuple(krl_struct.keys())
        var_type = self._get_var_type_by_struct_members(keys)
        return self.get_var_by_type(krl_struct, var_type)


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
            childResult = self.visit(c)
            if childResult is not None:
                result = childResult
        return result

    def visitChild(self, ctx, index=0):
        return self.visit(ctx.getChild(index))

    def visitTerminal(self, node):
        return node.getText()

    # TODO >> String literals should be checked if they have apostrophes inside, need to find out how it works on KUKA
    def _parse_simple_literal(self, ctx: krlParser.LiteralContext):
        parse = {
                krlLexer.INTLITERAL: lambda val: int(val),
                krlLexer.FLOATLITERAL: lambda val: float(val),
                krlLexer.TRUE: lambda val: True,
                krlLexer.FALSE: lambda val: False,
                krlLexer.CHARLITERAL: lambda val: val[1:-1],
                krlLexer.STRINGLITERAL: lambda val: val[1:-1]
                }
        literal_type = ctx.getChild(0).symbol.type
        value = ctx.getText()
        return parse[literal_type](value)

    def visitModuleName(self, ctx: krlParser.ModuleNameContext):
        return self.visit(ctx.IDENTIFIER())

    def visitVariableInitialisation(self, ctx: krlParser.VariableInitialisationContext):
        return self.visit(ctx.unaryPlusMinuxExpression())

    def visitModuleData(self, ctx: krlParser.ModuleDataContext):
        scope_name = self.visit(ctx.moduleName())
        a_record = ActivationRecord(name=scope_name, type_=ARType.MODULE, nesting_level=1, enclosing_ar=self._callstack.peek())
        self._callstack.push(a_record)
        self.visitChildren(ctx)
        #self._callstack.pop()

    def visitSubprogramCall(self, ctx: krlParser.SubprogramCallContext):
        #unlikely or even impossible (no examples in robot backup) routine calls with dot like "module.function()"
        routine_name = self.visit(ctx.variableName()[0])
        routine_symbol = self._current_symtable.lookup(routine_name)
        if routine_symbol:
            self.visit(routine_symbol.module_ctx)
            self.visit(routine_symbol.ctx)
        return self.visitChildren(ctx)

    # METHODS UNDER ARE COVERED WITH UNIT TESTS
    def visitStructLiteral(self, ctx: krlParser.StructLiteralContext):
        var_type: str = self.visit(ctx.typeName()) if ctx.typeName() else None
        var_value: dict = self.visit(ctx.structElementList())
        return self._var_factory.get_var_by_type(var_value, var_type) if var_type else var_value

    #TODO >> varlistrest to be implemented
    def visitVariableDeclarationInDataList(self, ctx: krlParser.VariableDeclarationInDataListContext):
        if ctx.DECL():
            var_type = self.visit(ctx.typeVar())
            var_name = self.visit(ctx.variableName())
            var_list_rest = ctx.variableListRest()
            ar = self._callstack.peek()
            if ctx.variableInitialisation():
                value = self.visit(ctx.variableInitialisation())
                if type(value) == dict:
                    value = self._var_factory.get_var_by_type(value, var_type)
                ar.initialize_var(var_name, value)

    def visitLiteral(self, ctx: krlParser.LiteralContext):
        literal_is_compound = ctx.structLiteral() or ctx.enumElement()
        return self.visitChild(ctx) if literal_is_compound else self._parse_simple_literal(ctx)

    def visitEnumElement(self, ctx: krlParser.EnumElementContext):
        identifier = self.visit(ctx.IDENTIFIER())
        return KrlEnum(str(identifier))

    def visitStructElementList(self, ctx: krlParser.StructElementListContext):
        struct_elements = {}
        for struct_elem in ctx.structElement():
            element = self.visit(struct_elem)
            struct_elements.update(element)
        return struct_elements

    def visitStructElement(self, ctx: krlParser.StructElementContext):
        key = self.visit(ctx.variableName())
        val = self.visit(ctx.unaryPlusMinuxExpression())
        return {key: val}

    def visitUnaryPlusMinuxExpression(self, ctx: krlParser.UnaryPlusMinuxExpressionContext):
        if ctx.primary():
            return self.visitChildren(ctx)
        else:
            return int(self.visitChild(ctx, 0) + '1') * self.visitChild(ctx, 1)

    def visitPtpMove(self, ctx: krlParser.PtpMoveContext):
        # TODO >> C_DIS/C_PTP should be checked (usually third child in ctx)
        # TODO >> Other drivable points to be implemented - like FRAME, or E3POS
        target = self.visit(ctx.geometricExpression())
        target_e6pos = self._var_factory.get_var_by_discover(target) if type(target) == dict else target
        logger.debug(f"Robot goes with PTP movement to: {target_e6pos}")
        calc_axes = self.ik_solver.perform_ik(target_e6pos, prev_e6_axis=E6Axis(axis_values=(0, 0, 0, 0, 0, 0)))
        ar = self._callstack.peek()
        ar["$POS_ACT"] = target_e6pos
        ar["$AXIS_ACT"] = calc_axes
        logger.debug(calc_axes)

    # TODO >> Type check INT=INT CHAR=CHAR INT=CHAR..
    def visitAssignmentExpression(self, ctx: krlParser.AssignmentExpressionContext):
        var_name = self.visit(ctx.leftHandSide())
        value = self.visit(ctx.expression()[0])
        ar = self._callstack.peek()
        ar[var_name] = value

    def visitVariableCall(self, ctx: krlParser.VariableCallContext):
        ar = self._callstack.peek()
        var_name = self.visit(ctx.variableName())
        logger.debug(f"Variable value resolved - {var_name}:{ar[var_name]}")
        return ar[var_name]

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
