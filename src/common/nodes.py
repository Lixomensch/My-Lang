class NumberNode:
    def __init__(self, value): self.value = value

class StringNode:
    def __init__(self, value): self.value = value

class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

class UnaryOpNode:
    def __init__(self, op, operand):
        self.op, self.operand = op, operand

class VarDeclNode:
    def __init__(self, name, expr): self.name, self.expr = name, expr

class AssignmentNode:
    def __init__(self, name, expr): self.name, self.expr = name, expr

class IfNode:
    def __init__(self, cond, then_block, else_block=None):
        self.cond, self.then_block, self.else_block = cond, then_block, else_block

class WhileNode:
    def __init__(self, cond, body): self.cond, self.body = cond, body

class FuncDeclNode:
    def __init__(self, name, params, body): self.name, self.params, self.body = name, params, body

class FuncCallNode:
    def __init__(self, name, args): self.name, self.args = name, args

class PrintNode:
    def __init__(self, expr): self.expr = expr

class InputNode:
    def __init__(self, prompt): self.prompt = prompt

class BlockNode:
    def __init__(self, statements): self.statements = statements

class VarAccessNode:
    def __init__(self, name): self.name = name