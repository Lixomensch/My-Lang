import ply.yacc as yacc
from .lexer import tokens
from .nodes import *

# ====================
# File: parser.py
# ====================

# Operator precedence
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQEQ', 'NEQ'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('right', 'NOT', 'UMINUS'),
)

# Internal storage for error reporting
_parser_data = ''

# Utility to compute column number

def _find_column(input_data, lexpos):
    last_cr = input_data.rfind('\n', 0, lexpos)
    if last_cr < 0:
        last_cr = -1
    return lexpos - last_cr

# Grammar rules

def p_program(p):
    'program : statement_list'
    p[0] = BlockNode(p[1])

# Statement list (possibly empty)

def p_statement_list(p):
    'statement_list : statement_list statement'
    p[0] = p[1] + [p[2]]

def p_statement_list_empty(p):
    'statement_list :'
    p[0] = []

# Variable declaration

def p_statement_var(p):
    'statement : VAR IDENTIFIER EQ expression SEMI'
    p[0] = VarDeclNode(p[2], p[4])

# Assignment

def p_statement_assign(p):
    'statement : IDENTIFIER EQ expression SEMI'
    p[0] = AssignmentNode(p[1], p[3])

# If statement

def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE else_part'
    then_block = BlockNode(p[6])
    else_block = BlockNode(p[8]) if p[8] is not None else None
    p[0] = IfNode(p[3], then_block, else_block)

def p_else_part(p):
    'else_part : ELSE LBRACE statement_list RBRACE'
    p[0] = p[3]

def p_else_part_empty(p):
    'else_part :'
    p[0] = None

# While loop

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE'
    p[0] = WhileNode(p[3], BlockNode(p[6]))

# Function declaration

def p_statement_func_decl(p):
    'statement : FUNC IDENTIFIER LPAREN parameters RPAREN LBRACE statement_list RBRACE'
    p[0] = FuncDeclNode(p[2], p[4], p[7])

# Parameters

def p_parameters(p):
    'parameters : IDENTIFIER'
    p[0] = [p[1]]

def p_parameters_list(p):
    'parameters : parameters COMMA IDENTIFIER'
    p[0] = p[1] + [p[3]]

def p_parameters_empty(p):
    'parameters :'
    p[0] = []

# Function call as statement

def p_statement_func_call(p):
    'statement : func_call SEMI'
    p[0] = p[1]

# Function call

def p_func_call(p):
    'func_call : IDENTIFIER LPAREN arguments RPAREN'
    p[0] = FuncCallNode(p[1], p[3])

# Expressions for input (returns string)
def p_expression_input(p):
    'expression : INPUT LPAREN STRING RPAREN'
    p[0] = InputNode(p[3])

# Arguments

def p_arguments(p):
    'arguments : expression'
    p[0] = [p[1]]

def p_arguments_list(p):
    'arguments : arguments COMMA expression'
    p[0] = p[1] + [p[3]]

def p_arguments_empty(p):
    'arguments :'
    p[0] = []

# Print statement

def p_statement_print(p):
    'statement : PRINT LPAREN expression RPAREN SEMI'
    p[0] = PrintNode(p[3])

# Input statement as standalone

def p_statement_input(p):
    'statement : INPUT LPAREN STRING RPAREN SEMI'
    p[0] = InputNode(p[3])

# Expressions

def p_expression_binop(p):
    '''expression : expression PLUS expression
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
                  | expression OR expression'''
    p[0] = BinaryOpNode(p[1], p[2], p[3])


def p_expression_unary(p):
    '''expression : NOT expression
                  | MINUS expression %prec UMINUS'''
    p[0] = UnaryOpNode(p[1], p[2])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = NumberNode(p[1])


def p_expression_string(p):
    'expression : STRING'
    p[0] = StringNode(p[1])


def p_expression_var(p):
    'expression : IDENTIFIER'
    p[0] = VarAccessNode(p[1])


def p_expression_func_call(p):
    'expression : func_call'
    p[0] = p[1]

# Error handling for syntax errors
def p_error(p):
    if p:
        col = _find_column(_parser_data, p.lexpos)
        line = p.lineno
        start = _parser_data.rfind('\n', 0, p.lexpos) + 1
        end = _parser_data.find('\n', p.lexpos)
        if end < 0:
            end = len(_parser_data)
        err_line = _parser_data[start:end]
        marker = ' ' * (col - 1) + '^'
        print(f"Syntax error at line {line}, column {col}: unexpected token '{p.value}' (type={p.type})")
        print(err_line)
        print(marker)
    else:
        print("Syntax error at EOF")

# Build parser and expose parse()
parser = yacc.yacc()

def parse(input_data, **kwargs):
    global _parser_data
    _parser_data = input_data
    return parser.parse(input_data, **kwargs)
