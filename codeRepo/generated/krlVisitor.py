# Generated from D:/Programowanie/PycharmProjects/KRL_Parser/codeRepo/generated\krl.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .krlParser import krlParser
else:
    from krlParser import krlParser

# This class defines a complete generic visitor for a parse tree produced by krlParser.

class krlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by krlParser#module.
    def visitModule(self, ctx:krlParser.ModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#moduleRoutines.
    def visitModuleRoutines(self, ctx:krlParser.ModuleRoutinesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#mainRoutine.
    def visitMainRoutine(self, ctx:krlParser.MainRoutineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#subRoutine.
    def visitSubRoutine(self, ctx:krlParser.SubRoutineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#procedureDefinition.
    def visitProcedureDefinition(self, ctx:krlParser.ProcedureDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#procedureName.
    def visitProcedureName(self, ctx:krlParser.ProcedureNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:krlParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#functionName.
    def visitFunctionName(self, ctx:krlParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#moduleData.
    def visitModuleData(self, ctx:krlParser.ModuleDataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#moduleName.
    def visitModuleName(self, ctx:krlParser.ModuleNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#dataList.
    def visitDataList(self, ctx:krlParser.DataListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#arrayInitialisation.
    def visitArrayInitialisation(self, ctx:krlParser.ArrayInitialisationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:krlParser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#structureDefinition.
    def visitStructureDefinition(self, ctx:krlParser.StructureDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#enumDefinition.
    def visitEnumDefinition(self, ctx:krlParser.EnumDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#enumValue.
    def visitEnumValue(self, ctx:krlParser.EnumValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:krlParser.VariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#signalDeclaration.
    def visitSignalDeclaration(self, ctx:krlParser.SignalDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#variableDeclarationInDataList.
    def visitVariableDeclarationInDataList(self, ctx:krlParser.VariableDeclarationInDataListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#variableListRest.
    def visitVariableListRest(self, ctx:krlParser.VariableListRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#variableInitialisation.
    def visitVariableInitialisation(self, ctx:krlParser.VariableInitialisationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#structLiteral.
    def visitStructLiteral(self, ctx:krlParser.StructLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#structElementList.
    def visitStructElementList(self, ctx:krlParser.StructElementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#structElement.
    def visitStructElement(self, ctx:krlParser.StructElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#formalParameters.
    def visitFormalParameters(self, ctx:krlParser.FormalParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#parameter.
    def visitParameter(self, ctx:krlParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#routineBody.
    def visitRoutineBody(self, ctx:krlParser.RoutineBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#routineDataSection.
    def visitRoutineDataSection(self, ctx:krlParser.RoutineDataSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#forwardDeclaration.
    def visitForwardDeclaration(self, ctx:krlParser.ForwardDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#formalParametersWithType.
    def visitFormalParametersWithType(self, ctx:krlParser.FormalParametersWithTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#parameterWithType.
    def visitParameterWithType(self, ctx:krlParser.ParameterWithTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#parameterCallType.
    def visitParameterCallType(self, ctx:krlParser.ParameterCallTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#importStatement.
    def visitImportStatement(self, ctx:krlParser.ImportStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#variableName.
    def visitVariableName(self, ctx:krlParser.VariableNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#arrayVariableSuffix.
    def visitArrayVariableSuffix(self, ctx:krlParser.ArrayVariableSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#routineImplementationSection.
    def visitRoutineImplementationSection(self, ctx:krlParser.RoutineImplementationSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#statementList.
    def visitStatementList(self, ctx:krlParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#continueStatement.
    def visitContinueStatement(self, ctx:krlParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#exitStatement.
    def visitExitStatement(self, ctx:krlParser.ExitStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#forLoop.
    def visitForLoop(self, ctx:krlParser.ForLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#goto.
    def visitGoto(self, ctx:krlParser.GotoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#halt.
    def visitHalt(self, ctx:krlParser.HaltContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#ifStatement.
    def visitIfStatement(self, ctx:krlParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#loop.
    def visitLoop(self, ctx:krlParser.LoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#repeat.
    def visitRepeat(self, ctx:krlParser.RepeatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#switch.
    def visitSwitch(self, ctx:krlParser.SwitchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#waitFor.
    def visitWaitFor(self, ctx:krlParser.WaitForContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#waitSec.
    def visitWaitSec(self, ctx:krlParser.WaitSecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#whileLoop.
    def visitWhileLoop(self, ctx:krlParser.WhileLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#returnStatement.
    def visitReturnStatement(self, ctx:krlParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#brakeStatement.
    def visitBrakeStatement(self, ctx:krlParser.BrakeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#assignment.
    def visitAssignment(self, ctx:krlParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#gotoBlock.
    def visitGotoBlock(self, ctx:krlParser.GotoBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#newl.
    def visitNewl(self, ctx:krlParser.NewlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#interruptDecl.
    def visitInterruptDecl(self, ctx:krlParser.InterruptDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#interrupt.
    def visitInterrupt(self, ctx:krlParser.InterruptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#ptpMove.
    def visitPtpMove(self, ctx:krlParser.PtpMoveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#ptpRelMove.
    def visitPtpRelMove(self, ctx:krlParser.PtpRelMoveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#linMove.
    def visitLinMove(self, ctx:krlParser.LinMoveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#linRelMove.
    def visitLinRelMove(self, ctx:krlParser.LinRelMoveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#circMove.
    def visitCircMove(self, ctx:krlParser.CircMoveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#trigger.
    def visitTrigger(self, ctx:krlParser.TriggerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#anInputStatement.
    def visitAnInputStatement(self, ctx:krlParser.AnInputStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#anOutStatement.
    def visitAnOutStatement(self, ctx:krlParser.AnOutStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#analogOutputStatement.
    def visitAnalogOutputStatement(self, ctx:krlParser.AnalogOutputStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#analogInputStatement.
    def visitAnalogInputStatement(self, ctx:krlParser.AnalogInputStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#switchBlockStatementGroups.
    def visitSwitchBlockStatementGroups(self, ctx:krlParser.SwitchBlockStatementGroupsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#caseLabel.
    def visitCaseLabel(self, ctx:krlParser.CaseLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#defaultLabel.
    def visitDefaultLabel(self, ctx:krlParser.DefaultLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#expressionList.
    def visitExpressionList(self, ctx:krlParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:krlParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#expression.
    def visitExpression(self, ctx:krlParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#relationalOp.
    def visitRelationalOp(self, ctx:krlParser.RelationalOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#conditionalOrExpression.
    def visitConditionalOrExpression(self, ctx:krlParser.ConditionalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#exclusiveOrExpression.
    def visitExclusiveOrExpression(self, ctx:krlParser.ExclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#conditionalAndExpression.
    def visitConditionalAndExpression(self, ctx:krlParser.ConditionalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:krlParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:krlParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#geometricExpression.
    def visitGeometricExpression(self, ctx:krlParser.GeometricExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#unaryNotExpression.
    def visitUnaryNotExpression(self, ctx:krlParser.UnaryNotExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#unaryPlusMinuxExpression.
    def visitUnaryPlusMinuxExpression(self, ctx:krlParser.UnaryPlusMinuxExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#primary.
    def visitPrimary(self, ctx:krlParser.PrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#parExpression.
    def visitParExpression(self, ctx:krlParser.ParExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#typeVar.
    def visitTypeVar(self, ctx:krlParser.TypeVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#typeName.
    def visitTypeName(self, ctx:krlParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#primitiveType.
    def visitPrimitiveType(self, ctx:krlParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#arguments.
    def visitArguments(self, ctx:krlParser.ArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#literal.
    def visitLiteral(self, ctx:krlParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by krlParser#enumElement.
    def visitEnumElement(self, ctx:krlParser.EnumElementContext):
        return self.visitChildren(ctx)



del krlParser