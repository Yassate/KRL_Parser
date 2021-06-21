from krlVisitor import krlVisitor
from krlLexer import krlLexer
from krlParser import krlParser
from callstack import ActivationRecord, ARType
from kuka_datatypes import E6Pos, E6Axis, KrlEnum
import coloredlogs, logging

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
            childResult = c.accept(self)
            if childResult is not None:
                result = childResult
        return result

    def visitChild(self, ctx, index=0):
        return ctx.getChild(index).accept(self)

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
        return ctx.IDENTIFIER().accept(self)

    def visitVariableInitialisation(self, ctx: krlParser.VariableInitialisationContext):
        return ctx.unaryPlusMinuxExpression().accept(self)

    def visitModuleData(self, ctx: krlParser.ModuleDataContext):
        scope_name = ctx.moduleName().accept(self)
        a_record = ActivationRecord(name=scope_name, type_=ARType.MODULE, nesting_level=1, enclosing_ar=self._callstack.peek())
        self._callstack.push(a_record)
        self.visitChildren(ctx)

    def visitEnumElement(self, ctx:krlParser.EnumElementContext):
        return self.visitChildren(ctx)

    # METHODS UNDER ARE COVERED WITH UNITTESTS

    def visitStructLiteral(self, ctx: krlParser.StructLiteralContext):
        var_type: str = ctx.typeName().accept(self) if ctx.typeName() else None
        var_value: dict = ctx.structElementList().accept(self)
        return self._var_factory.get_var_by_type(var_value, var_type) if var_type else var_value

    #TODO >> varlistrest to be implemented
    def visitVariableDeclarationInDataList(self, ctx: krlParser.VariableDeclarationInDataListContext):
        if ctx.DECL():
            var_type = ctx.typeVar().accept(self)
            var_name = ctx.variableName().accept(self)
            var_list_rest = ctx.variableListRest()
            ar = self._callstack.peek()
            if ctx.variableInitialisation():
                value = ctx.variableInitialisation().accept(self)
                if type(value) == dict:
                    value = self._var_factory.get_var_by_type(value, var_type)
                ar.initialize_var(var_name, value)

            #if var_list_rest is not None:
                #for name in var_list_rest.accept(self):
                    #pass

    # TODO >> Enum literal visitor
    def visitLiteral(self, ctx: krlParser.LiteralContext):
        literal_is_compound = ctx.structLiteral() or ctx.enumElement()
        return self.visitChild(ctx) if literal_is_compound else self._parse_simple_literal(ctx)

    def visitEnumElement(self, ctx: krlParser.EnumElementContext):
        return KrlEnum(str(ctx.IDENTIFIER()))

    def visitStructElementList(self, ctx: krlParser.StructElementListContext):
        struct_elements = {}
        for struct_elem in ctx.structElement():
            element = struct_elem.accept(self)
            struct_elements.update(element)
        return struct_elements

    def visitStructElement(self, ctx: krlParser.StructElementContext):
        key = ctx.variableName().accept(self)
        val = ctx.unaryPlusMinuxExpression().accept(self)
        return {key: val}

    def visitUnaryPlusMinuxExpression(self, ctx: krlParser.UnaryPlusMinuxExpressionContext):
        if ctx.primary():
            return self.visitChildren(ctx)
        else:
            return int(ctx.getChild(0).accept(self) + '1') * ctx.getChild(1).accept(self)

    def visitPtpMove(self, ctx: krlParser.PtpMoveContext):
        # TODO >> C_DIS/C_PTP should be checked (usually third child in ctx)
        # TODO >> Other drivable points to be implemented - like FRAME, or E3POS
        target = ctx.geometricExpression().accept(self)
        target_e6pos = self._var_factory.get_var_by_discover(target) if type(target) == dict else target
        logger.debug(f"Robot goes with PTP movement to: {target_e6pos}")
        calc_axes = self.ik_solver.perform_ik(target_e6pos, prev_e6_axis=E6Axis(axis_values=(0, 0, 0, 0, 0, 0)))
        ar = self._callstack.peek()
        ar["$POS_ACT"] = target_e6pos
        ar["$AXIS_ACT"] = calc_axes
        logger.debug(calc_axes)

    # TODO >> Type check INT=INT CHAR=CHAR INT=CHAR..
    def visitAssignmentExpression(self, ctx: krlParser.AssignmentExpressionContext):
        var_name = ctx.leftHandSide().accept(self)
        value = ctx.expression()[0].accept(self)
        ar = self._callstack.peek()
        ar[var_name] = value

    # TODO >> All .accept(self) should be changed to visit(ctx.....)
    def visitVariableCall(self, ctx: krlParser.VariableCallContext):
        ar = self._callstack.peek()
        var_name = self.visit(ctx.variableName())
        return ar[var_name]

    def visitVariableName(self, ctx: krlParser.VariableNameContext):
        var_name = ctx.IDENTIFIER().getText()
        var_suffix = ctx.arrayVariableSuffix()
        indices = var_suffix.accept(self) if var_suffix else ''
        return var_name + indices

    def visitArrayVariableSuffix(self, ctx: krlParser.ArrayVariableSuffixContext):
        indices = []
        for i in range(len(ctx.children)):
            indices.append(self.visitChild(ctx, i))
        return ''.join(map(str, indices))
