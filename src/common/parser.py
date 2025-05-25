"""Parser for the simple language."""

from ply import yacc

from .lexer import tokens  # pylint: disable=W0611
from .nodes import *

precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("left", "EQEQ", "NEQ"),
    ("left", "LT", "LE", "GT", "GE"),
    ("left", "PLUS", "MINUS"),
    ("left", "MUL", "DIV"),
    ("right", "NOT", "UMINUS"),
)

_PARSER_DATA = ""


def _find_column(input_data, lexpos):
    """
    Calculate the column number of a given position in the input data.

    Parameters:
    input_data (str): The input data string.
    lexpos (int): The position in the input data for which to find the column number.

    Returns:
    int: The column number corresponding to the given position.
    """
    last_cr = input_data.rfind("\n", 0, lexpos)
    if last_cr < 0:
        last_cr = -1
    return lexpos - last_cr


def p_program(p):
    "program : statement_list"
    p[0] = BlockNode(p[1])


def p_statement_list(p):
    "statement_list : statement_list statement"
    p[0] = p[1] + [p[2]]


def p_statement_list_empty(p):
    "statement_list :"
    p[0] = []


def p_statement_var(p):
    "statement : VAR IDENTIFIER EQ expression SEMI"
    p[0] = VarDeclNode(p[2], p[4])


def p_statement_assign(p):
    "statement : IDENTIFIER EQ expression SEMI"
    p[0] = AssignmentNode(p[1], p[3])


def p_statement_if(p):
    "statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE else_part"
    then_block = BlockNode(p[6])
    else_block = BlockNode(p[8]) if p[8] is not None else None
    p[0] = IfNode(p[3], then_block, else_block)


def p_else_part(p):
    "else_part : ELSE LBRACE statement_list RBRACE"
    p[0] = p[3]


def p_else_part_empty(p):
    "else_part :"
    p[0] = None


def p_statement_while(p):
    "statement : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE"
    p[0] = WhileNode(p[3], BlockNode(p[6]))


def p_statement_func_decl(p):
    "statement : FUNC IDENTIFIER LPAREN parameters RPAREN LBRACE statement_list RBRACE"
    p[0] = FuncDeclNode(p[2], p[4], p[7])


def p_parameters(p):
    "parameters : IDENTIFIER"
    p[0] = [p[1]]


def p_parameters_list(p):
    "parameters : parameters COMMA IDENTIFIER"
    p[0] = p[1] + [p[3]]


def p_parameters_empty(p):
    "parameters :"
    p[0] = []


def p_statement_func_call(p):
    "statement : func_call SEMI"
    p[0] = p[1]


def p_func_call(p):
    "func_call : IDENTIFIER LPAREN arguments RPAREN"
    p[0] = FuncCallNode(p[1], p[3])


def p_expression_input(p):
    "expression : INPUT LPAREN STRING RPAREN"
    p[0] = InputNode(p[3])


def p_arguments(p):
    "arguments : expression"
    p[0] = [p[1]]


def p_arguments_list(p):
    "arguments : arguments COMMA expression"
    p[0] = p[1] + [p[3]]


def p_arguments_empty(p):
    "arguments :"
    p[0] = []


def p_statement_print(p):
    "statement : PRINT LPAREN expression RPAREN SEMI"
    p[0] = PrintNode(p[3])


def p_statement_input(p):
    "statement : INPUT LPAREN STRING RPAREN SEMI"
    p[0] = InputNode(p[3])


def p_expression_binop(p):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression MUL expression
    | expression DIV expression
    | expression EQEQ expression
    | expression NEQ expression
    | expression LT expression
    | expression LE expression
    | expression GT expression
    | expression GE expression
    | expression AND expression
    | expression OR expression"""
    p[0] = BinaryOpNode(p[1], p[2], p[3])


def p_expression_unary(p):
    """expression : NOT expression
    | MINUS expression %prec UMINUS"""
    p[0] = UnaryOpNode(p[1], p[2])


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = NumberNode(p[1])


def p_expression_string(p):
    "expression : STRING"
    p[0] = StringNode(p[1])


def p_expression_var(p):
    "expression : IDENTIFIER"
    p[0] = VarAccessNode(p[1])


def p_expression_func_call(p):
    "expression : func_call"
    p[0] = p[1]


def p_error(p):
    """
    Handle syntax errors.

    When a syntax error is encountered, print an error message with line and column information
    and a marker pointing to the location of the error.

    If the error is at the end of the file (i.e. p is None), print a different message.
    """
    if p:
        col = _find_column(_PARSER_DATA, p.lexpos)
        line = p.lineno
        start = _PARSER_DATA.rfind("\n", 0, p.lexpos) + 1
        end = _PARSER_DATA.find("\n", p.lexpos)
        if end < 0:
            end = len(_PARSER_DATA)
        err_line = _PARSER_DATA[start:end]
        marker = " " * (col - 1) + "^"
        print(
            f"Syntax error at line {line}, column {col}:"
            f" unexpected token '{p.value}' (type={p.type})"
        )
        print(err_line)
        print(marker)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


def parse(input_data, **kwargs):
    """
    Parse the given input data using the generated parser.

    This function takes in input data and arbitrary keyword arguments and passes them to the
    generated parser. The input data is stored in the global variable `_parser_data` for use by
    the `p_error` function when reporting syntax errors.

    :param input_data: The input data to be parsed.
    :param kwargs: Additional keyword arguments to pass to the parser.
    :return: The result of parsing the input data.
    """
    global _PARSER_DATA
    _PARSER_DATA = input_data
    return parser.parse(input_data, **kwargs)
