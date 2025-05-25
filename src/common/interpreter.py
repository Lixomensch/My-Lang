from common.nodes import *

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.funcs = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable '{name}'")

    def set(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise NameError(f"Undefined variable '{name}'")

    def define(self, name, value):
        self.vars[name] = value

    def define_func(self, name, func_node):
        self.funcs[name] = func_node

    def get_func(self, name):
        if name in self.funcs:
            return self.funcs[name]
        if self.parent:
            return self.parent.get_func(name)
        raise NameError(f"Undefined function '{name}'")

# Helper to convert strings to numbers

def _to_number(val):
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
        self.global_env = Environment()

    def visit(self, node, env=None):
        if env is None:
            env = self.global_env
        method_name = f"visit_{type(node).__name__}"
        if not hasattr(self, method_name):
            raise Exception(f"No visit method for {type(node).__name__}")
        return getattr(self, method_name)(node, env)

    def visit_BlockNode(self, node, env):
        result = None
        for stmt in node.statements:
            result = self.visit(stmt, env)
        return result

    def visit_VarDeclNode(self, node, env):
        value = self.visit(node.expr, env) if node.expr is not None else None
        env.define(node.name, value)

    def visit_AssignmentNode(self, node, env):
        value = self.visit(node.expr, env)
        env.set(node.name, value)

    def visit_NumberNode(self, node, env):
        return node.value

    def visit_StringNode(self, node, env):
        return node.value

    def visit_VarAccessNode(self, node, env):
        # boolean literals
        if node.name == 'true':
            return True
        if node.name == 'false':
            return False
        return env.get(node.name)

    def visit_BinaryOpNode(self, node, env):
        left = self.visit(node.left, env)
        right = self.visit(node.right, env)
        op = node.op
        # '+' supports numeric addition with conversion or string concatenation
        if op == '+':
            lnum = _to_number(left)
            rnum = _to_number(right)
            if lnum is not None and rnum is not None:
                return lnum + rnum
            return str(left) + str(right)
        if op == '-':
            lnum = _to_number(left)
            rnum = _to_number(right)
            return lnum - rnum
        if op == '*': return left * right
        if op == '/': return left / right
        if op == '==': return left == right
        if op == '!=': return left != right
        if op == '<': return left < right
        if op == '<=': return left <= right
        if op == '>': return left > right
        if op == '>=': return left >= right
        if op == 'and': return bool(left) and bool(right)
        if op == 'or': return bool(left) or bool(right)
        raise Exception(f"Unknown binary operator: {op}")

    def visit_UnaryOpNode(self, node, env):
        operand = self.visit(node.operand, env)
        op = node.op
        if op == '-': return -operand
        if op == 'not': return not operand
        if op == '+': return +operand
        raise Exception(f"Unknown unary operator: {op}")

    def visit_IfNode(self, node, env):
        cond = self.visit(node.cond, env)
        if cond:
            return self.visit(node.then_block, Environment(env))
        elif node.else_block:
            return self.visit(node.else_block, Environment(env))

    def visit_WhileNode(self, node, env):
        result = None
        while self.visit(node.cond, env):
            result = self.visit(node.body, Environment(env))
        return result

    def visit_FuncDeclNode(self, node, env):
        env.define_func(node.name, node)

    def visit_FuncCallNode(self, node, env):
        if node.name == 'print':
            value = self.visit(node.args[0], env)
            print(value)
            return None
        if node.name == 'input':
            prompt = self.visit(node.args[0], env)
            return input(prompt)
        func = env.get_func(node.name)
        new_env = Environment(env)
        for param, arg in zip(func.params, node.args):
            new_env.define(param, self.visit(arg, env))
        return self.visit(BlockNode(func.body), new_env)

    def visit_PrintNode(self, node, env):
        value = self.visit(node.expr, env)
        print(value)

    def visit_InputNode(self, node, env):
        prompt = node.prompt
        return input(prompt)
