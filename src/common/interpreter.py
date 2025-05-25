"""Interpreter for the MyLang language."""

from common.nodes import BlockNode


# pylint: disable=C0103
class Environment:
    def __init__(self, parent=None):
        """Initializes a new Environment.

        :param parent: The parent environment, defaults to None.
        """
        self.vars = {}
        self.funcs = {}
        self.parent = parent

    def get(self, name):
        """
        Retrieves the value of a variable by its name from the current environment.

        :param name: The name of the variable to retrieve.
        :return: The value of the variable.
        :raises NameError: If the variable is not found in the current or any parent environment.
        """
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable '{name}'")

    def set(self, name, value):
        """
        Sets the value of a variable by its name in the current environment.

        :param name: The name of the variable to set.
        :param value: The value to set the variable to.
        :raises NameError: If the variable is not found in the current or any parent environment.
        """
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise NameError(f"Undefined variable '{name}'")

    def define(self, name, value):
        """
        Defines a new variable in the current environment.

        :param name: The name of the variable to define.
        :param value: The value to assign to the variable.
        """
        self.vars[name] = value

    def define_func(self, name, func_node):
        """
        Defines a new function in the current environment.

        :param name: The name of the function to define.
        :param func_node: The function node to assign to the name.
        """
        self.funcs[name] = func_node

    def get_func(self, name):
        """
        Retrieves the function node of a function by its name from the current environment.

        :param name: The name of the function to retrieve.
        :return: The function node of the function.
        :raises NameError: If the function is not found in the current or any parent environment.
        """
        if name in self.funcs:
            return self.funcs[name]
        if self.parent:
            return self.parent.get_func(name)
        raise NameError(f"Undefined function '{name}'")


def _to_number(val):
    """
    Converts a given value to a number (int or float) if possible.

    :param val: The value to convert.
    :return: The converted number, or None if it could not be converted.
    """
    if isinstance(val, (int, float)):
        return val
    if isinstance(val, str):
        try:
            return int(val)
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return None
    return None


class Interpreter:
    def __init__(self):
        """
        Initializes a new Interpreter.

        Creates a new global environment and assigns it to the global_env attribute.
        """
        self.global_env = Environment()

    def visit(self, node, env=None):
        """
        Visits a node in the AST and executes the corresponding visit method.

        This method determines the type of the node and dynamically calls the appropriate
        visit method implemented for that specific node type.

        :param node: The AST node to visit.
        :param env: The environment in which to evaluate the node. If not provided, the global
                    environment is used by default.
        :return: The result of visiting the node, which may vary depending on the node type.
        :raises Exception: If there is no visit method implemented for the node's type.
        """
        if env is None:
            env = self.global_env
        method_name = f"visit_{type(node).__name__}"
        if not hasattr(self, method_name):
            raise Exception(f"No visit method for {type(node).__name__}")
        return getattr(self, method_name)(node, env)

    def visit_BlockNode(self, node, env):
        """
        Visits a BlockNode and executes each statement in the block.

        This method iterates over the statements in the BlockNode and visits each one
        using the provided environment. The result of the last executed statement is returned.

        :param node: The BlockNode containing the list of statements to execute.
        :param env: The environment in which to evaluate the statements.
        :return: The result of the last statement in the block.
        """
        result = None
        for stmt in node.statements:
            result = self.visit(stmt, env)
        return result

    def visit_VarDeclNode(self, node, env):
        """
        Visits a VarDeclNode and defines a new variable in the current environment.

        This method visits the expression in the VarDeclNode (if it exists) and assigns
        the result to the variable being declared. If the expression is None, the variable
        is given a value of None.

        :param node: The VarDeclNode containing the name and expression to evaluate.
        :param env: The environment in which to define the variable.
        :return: None
        """
        value = self.visit(node.expr, env) if node.expr is not None else None
        env.define(node.name, value)

    def visit_AssignmentNode(self, node, env):
        """
        Visits an AssignmentNode and assigns the value of the expression to the variable.

        This method visits the expression in the AssignmentNode and assigns the result to the
        variable using the set method of the environment.

        :param node: The AssignmentNode containing the name and expression to evaluate.
        :param env: The environment in which to define the variable.
        :return: None
        """
        value = self.visit(node.expr, env)
        env.set(node.name, value)

    def visit_NumberNode(self, node, _env):
        """
        Visits a NumberNode and returns the value of the node.

        This method simply returns the value of the node without any additional computation.

        :param node: The NumberNode containing the value to return.
        :param env: The environment in which to evaluate the node.
        :return: The value of the node.
        """
        return node.value

    def visit_StringNode(self, node, _env):
        """
        Visits a StringNode and returns the value of the node.

        This method simply returns the value of the node without any additional computation.

        :param node: The StringNode containing the value to return.
        :param env: The environment in which to evaluate the node.
        :return: The value of the node.
        """
        return node.value

    def visit_VarAccessNode(self, node, env):
        """
        Visits a VarAccessNode and returns the value of the variable.

        This method visits a VarAccessNode and returns the value of the variable
        referenced by the node. If the variable is not found in the current or
        any parent environment, a NameError is raised.

        :param node: The VarAccessNode containing the name of the variable to access.
        :param env: The environment in which to access the variable.
        :return: The value of the variable.
        :raises NameError: If the variable is not found in the current or any parent environment.
        """
        if node.name == "true":
            return True
        if node.name == "false":
            return False
        return env.get(node.name)

    # pylint: disable=R0911,R0912
    def visit_BinaryOpNode(self, node, env):
        """
        Visits a BinaryOpNode and evaluates the binary operation.

        This method evaluates the left and right operands of a BinaryOpNode
        and applies the specified binary operator. The supported operators
        include arithmetic operations (+, -, *, /), comparison operations
        (==, !=, <, <=, >, >=), and logical operations (and, or). It raises
        an exception for unknown operators.

        :param node: The BinaryOpNode containing the left operand, operator, and right operand.
        :param env: The environment in which to evaluate the operands.
        :return: The result of applying the binary operation on the operands.
        :raises Exception: If an unknown binary operator is encountered.
        """

        left = self.visit(node.left, env)
        right = self.visit(node.right, env)
        op = node.op
        if op == "+":
            lnum = _to_number(left)
            rnum = _to_number(right)
            if lnum is not None and rnum is not None:
                return lnum + rnum
            return str(left) + str(right)
        if op == "-":
            lnum = _to_number(left)
            rnum = _to_number(right)
            return lnum - rnum
        if op == "*":
            return left * right
        if op == "/":
            return left / right
        if op == "==":
            return left == right
        if op == "!=":
            return left != right
        if op == "<":
            return left < right
        if op == "<=":
            return left <= right
        if op == ">":
            return left > right
        if op == ">=":
            return left >= right
        if op == "and":
            return bool(left) and bool(right)
        if op == "or":
            return bool(left) or bool(right)
        raise Exception(f"Unknown binary operator: {op}")

    def visit_UnaryOpNode(self, node, env):
        """
        Visits a UnaryOpNode and evaluates the unary operation.

        This method evaluates the operand of a UnaryOpNode and applies the specified unary
        operator. The supported operators include negation (-), logical not (not), and
        unary plus (+). It raises an exception for unknown operators.

        :param node: The UnaryOpNode containing the operand and operator to evaluate.
        :param env: The environment in which to evaluate the operand.
        :return: The result of applying the unary operation on the operand.
        :raises Exception: If an unknown unary operator is encountered.
        """
        operand = self.visit(node.operand, env)
        op = node.op
        if op == "-":
            return -operand
        if op == "not":
            return not operand
        if op == "+":
            return +operand
        raise Exception(f"Unknown unary operator: {op}")

    def visit_IfNode(self, node, env):
        """
        Visits an IfNode and evaluates the conditional expression.

        This method evaluates the condition of an IfNode and runs either the then-block
        or the else-block depending on the value of the condition. If the condition is
        true, the then-block is executed; otherwise, the else-block is executed if it
        exists.

        :param node: The IfNode containing the condition, then-block, and else-block.
        :param env: The environment in which to evaluate the condition.
        :return: The result of evaluating either the then-block or the else-block.
        """
        cond = self.visit(node.cond, env)
        if cond:
            return self.visit(node.then_block, Environment(env))
        if node.else_block:
            return self.visit(node.else_block, Environment(env))
        return None

    def visit_WhileNode(self, node, env):
        """
        Visits a WhileNode and evaluates the loop condition and body.

        This method evaluates the condition of a WhileNode and runs the body of the loop
        until the condition is false. If the condition is true, the body of the loop is
        executed; if it is false, the loop is terminated.

        :param node: The WhileNode containing the condition and body of the loop.
        :param env: The environment in which to evaluate the condition and body.
        :return: The result of evaluating the body of the loop the last time it was run.
        """
        result = None
        while self.visit(node.cond, env):
            result = self.visit(node.body, Environment(env))
        return result

    def visit_FuncDeclNode(self, node, env):
        """
        Visits a FuncDeclNode and defines a function in the current environment.

        This method registers a new function declaration by associating the function
        name with the FuncDeclNode. The function can be later called using the name
        in expressions.

        :param node: The FuncDeclNode containing the name and function details.
        :param env: The environment in which to define the function.
        :return: None
        """

        env.define_func(node.name, node)

    def visit_FuncCallNode(self, node, env):
        """
        Visits a FuncCallNode and evaluates the function call expression.

        This method calls a function by evaluating the arguments of the function call
        expression and passing them to the function. It returns the result of the
        function call expression.

        :param node: The FuncCallNode containing the function name and arguments.
        :param env: The environment in which to evaluate the arguments.
        :return: The result of evaluating the function call expression.
        """
        if node.name == "print":
            value = self.visit(node.args[0], env)
            print(value)
            return None
        if node.name == "input":
            prompt = self.visit(node.args[0], env)
            return input(prompt)
        func = env.get_func(node.name)
        new_env = Environment(env)
        for param, arg in zip(func.params, node.args):
            new_env.define(param, self.visit(arg, env))
        return self.visit(BlockNode(func.body), new_env)

    def visit_PrintNode(self, node, env):
        """
        Visits a PrintNode and evaluates the expression to print its value.

        This method evaluates the expression contained within a PrintNode and prints
        the resulting value to the console.

        :param node: The PrintNode containing the expression to evaluate and print.
        :param env: The environment in which to evaluate the expression.
        :return: None
        """

        value = self.visit(node.expr, env)
        print(value)

    def visit_InputNode(self, node, _env):
        """
        Visits an InputNode and evaluates the prompt expression to read input from the user.

        This method evaluates the prompt expression contained within an InputNode and
        prints the resulting value to the console. It then reads input from the user and
        returns the input value.

        :param node: The InputNode containing the prompt expression to evaluate and
                     print.
        :param env: The environment in which to evaluate the prompt expression.
        :return: The input value read from the user.
        """
        prompt = node.prompt
        return input(prompt)


# pylint: enable=c0103
