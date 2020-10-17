from krlVisitor import krlVisitor
from krlParser import krlParser

class krlVariable:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.value = None

class krlVisitorImpl(krlVisitor):
    def __init__(self):
        super().__init__()
        self.variables = []

    # Visit a parse tree produced by krlParser#variableDeclarationInDataList.
    def visitVariableDeclarationInDataList(self, ctx:krlParser.VariableDeclarationInDataListContext):
        print(ctx.getText())

        #CORRECT DECLARATION
        if ctx.children[0].getText() == "DECL":
            self.variables.append(krlVariable(ctx.children[1].getText(), ctx.children[2].getText()))
            print("Variable type: " + ctx.children[1].getText())
            print("Variable name: " + ctx.children[2].getText())
        #elif ctx.children[0].typeName() == "TypeVarContext":
            #print("type var context")
        #self.children[3].accept()
        #res = self.visitChildren(ctx)
        return self.visitChildren(ctx)

    #def visitVariableInitialisation(self, ctx:krlParser.VariableInitialisationContext):
        #return "5" + self.visitChildren(ctx)

    #def visitUnaryPlusMinuxExpression(self, ctx:krlParser.UnaryPlusMinuxExpressionContext):
        #return "87"

    #def visitTypeName(self, ctx:krlParser.TypeNameContext):
        #return 6

