import ply.lex as lex

tokens = [
    'NUMBER', 'STRING', 'IDENTIFIER',
    'PLUS', 'MINUS', 'MUL', 'DIV',
    'EQ', 'EQEQ', 'NEQ', 'LT', 'LE', 'GT', 'GE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'COMMA', 'SEMI'
]

reserved = {
    'var': 'VAR', 'if': 'IF', 'else': 'ELSE',
    'while': 'WHILE', 'func': 'FUNC',
    'print': 'PRINT', 'input': 'INPUT',
    'and': 'AND', 'or': 'OR', 'not': 'NOT'
}

tokens += list(reserved.values())

t_PLUS    = r"\+"
t_MINUS   = r"-"
t_MUL     = r"\*"
t_DIV     = r"/"
t_EQEQ    = r"=="
t_NEQ     = r"!="
t_LE      = r"<="
t_LT      = r"<"
t_GE      = r">="
t_GT      = r">"
t_EQ      = r"="
t_LPAREN  = r"\("
t_RPAREN  = r"\)"
t_LBRACE  = r"\{"
t_RBRACE  = r"\}"
t_COMMA   = r"," 
t_SEMI    = r";"

t_ignore = ' \t'

def t_NUMBER(t):
    r"\d+(\.\d+)?"
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'"([^\\"]|(\\.))*"'
    t.value = t.value[1:-1]
    return t

def t_IDENTIFIER(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_COMMENT(t):
    r"//.*"
    pass

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

def _find_column(input_data, lexpos):
    last_cr = input_data.rfind('\n', 0, lexpos)
    if last_cr < 0:
        last_cr = -1
    return lexpos - last_cr

def t_error(t):

    global _lexer_data
    if not _lexer_data:
        _lexer_data = t.lexer.lexdata
    line = t.lexer.lineno
    pos = t.lexer.lexpos
    col = _find_column(_lexer_data, pos)

    start = _lexer_data.rfind('\n', 0, pos) + 1
    end = _lexer_data.find('\n', pos)
    if end < 0:
        end = len(_lexer_data)
    err_line = _lexer_data[start:end]

    marker = ' ' * (col - 1) + '^'
    print(f"Lexical error at line {line}, column {col}: unexpected character '{t.value[0]}'")
    print(err_line)
    print(marker)
    t.lexer.skip(1)

def build_lexer(input_data=None, **kwargs):
    """
    Build and return a lexer. Optionally initialize with input_data (string) for improved errors.
    """
    global _lexer_data
    _lexer_data = input_data or ''
    lex_obj = lex.lex(**kwargs)
    if input_data is not None:
        lex_obj.input(input_data)
    return lex_obj

lexer = build_lexer()
