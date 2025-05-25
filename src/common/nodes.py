"""
This module contains classes representing different types of nodes in the abstract syntax tree.
"""


class NumberNode:
    def __init__(self, value):
        """
        Initializes a new NumberNode with the given value.

        :param value: The numerical value represented by this node.
        :type value: int | float
        """
        self.value = value


class StringNode:
    def __init__(self, value):
        """
        Initializes a new StringNode with the given value.

        :param value: The string value represented by this node.
        :type value: str
        """
        self.value = value


class BinaryOpNode:
    def __init__(self, left, op, right):
        """
        Initializes a new BinaryOpNode with the given left operand, operator, and right operand.

        :param left: The left operand of the binary operation.
        :type left: Node
        :param op: The operator to apply to the operands.
        :type op: str
        :param right: The right operand of the binary operation.
        :type right: Node
        """
        self.left, self.op, self.right = left, op, right


class UnaryOpNode:
    def __init__(self, op, operand):
        """
        Initializes a new UnaryOpNode with the given operator and operand.

        :param op: The operator to apply to the operand.
        :type op: str
        :param operand: The operand of the unary operation.
        :type operand: Node
        """
        self.op, self.operand = op, operand


class VarDeclNode:
    def __init__(self, name, expr):
        """
        Initializes a new VarDeclNode with the given name and expression.

        :param name: The name of the variable to declare.
        :type name: str
        :param expr: The expression to evaluate and assign to the variable.
        :type expr: Node
        """
        self.name, self.expr = name, expr


class AssignmentNode:
    def __init__(self, name, expr):
        """
        Initializes a new AssignmentNode with the given name and expression.

        :param name: The name of the variable to assign to.
        :type name: str
        :param expr: The expression to evaluate and assign to the variable.
        :type expr: Node
        """
        self.name, self.expr = name, expr


class IfNode:
    def __init__(self, cond, then_block, else_block=None):
        """
        Initializes a new IfNode with the given condition, then-block, and else-block.

        :param cond: The condition to evaluate.
        :type cond: Node
        :param then_block: The block of code to execute if the condition is true.
        :type then_block: BlockNode
        :param else_block: The block of code to execute if the condition is false.
                          Defaults to None.
        :type else_block: BlockNode or None
        """
        self.cond, self.then_block, self.else_block = cond, then_block, else_block


class WhileNode:
    def __init__(self, cond, body):
        """
        Initializes a new WhileNode with the given condition and body.

        :param cond: The condition to evaluate.
        :type cond: Node
        :param body: The block of code to execute while the condition is true.
        :type body: BlockNode
        """
        self.cond, self.body = cond, body


class FuncDeclNode:
    def __init__(self, name, params, body):
        """
        Initializes a new FuncDeclNode with the given name, parameters, and body.

        :param name: The name of the function to declare.
        :type name: str
        :param params: The parameters of the function.
        :type params: list of str
        :param body: The block of code to execute when the function is called.
        :type body: BlockNode
        """
        self.name, self.params, self.body = name, params, body


class FuncCallNode:
    def __init__(self, name, args):
        """
        Initializes a new FuncCallNode with the given function name and arguments.

        :param name: The name of the function to call.
        :type name: str
        :param args: The arguments to pass to the function call.
        :type args: list of Node
        """

        self.name, self.args = name, args


class PrintNode:
    def __init__(self, expr):
        """
        Initializes a new PrintNode with the given expression to print.

        :param expr: The expression to evaluate and print.
        :type expr: Node
        """
        self.expr = expr


class InputNode:
    def __init__(self, prompt):
        """
        Initializes a new InputNode with the given prompt expression.

        :param prompt: The expression to evaluate and use as the prompt for the input.
        :type prompt: Node
        """
        self.prompt = prompt


class BlockNode:
    def __init__(self, statements):
        """
        Initializes a new BlockNode with the given list of statements.

        :param statements: The list of statements to include in the block.
        :type statements: list of Node
        """
        self.statements = statements


class VarAccessNode:
    def __init__(self, name):
        """
        Initializes a new VarAccessNode with the given name.

        :param name: The name of the variable to access.
        :type name: str
        """
        self.name = name
