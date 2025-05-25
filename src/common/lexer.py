"""Lexer for the simple language."""

from ply import lex

_LEXER_DATA = ""

# pylint: disable=C0103
tokens = [
    "NUMBER",
    "STRING",
    "IDENTIFIER",
    "PLUS",
    "MINUS",
    "MUL",
    "DIV",
    "EQ",
    "EQEQ",
    "NEQ",
    "LT",
    "LE",
    "GT",
    "GE",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "COMMA",
    "SEMI",
]

reserved = {
    "var": "VAR",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "func": "FUNC",
    "print": "PRINT",
    "input": "INPUT",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
}

tokens += list(reserved.values())

t_PLUS = r"\+"
t_MINUS = r"-"
t_MUL = r"\*"
t_DIV = r"/"
t_EQEQ = r"=="
t_NEQ = r"!="
t_LE = r"<="
t_LT = r"<"
t_GE = r">="
t_GT = r">"
t_EQ = r"="
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_COMMA = r","
t_SEMI = r";"

t_ignore = " \t"
t_ignore_COMMENT = r"//.*"


def t_NUMBER(t):
    r"\d+(\.\d+)?"
    t.value = float(t.value) if "." in t.value else int(t.value)
    return t


def t_STRING(t):
    r'"([^\\"]|(\\.))*"'
    t.value = t.value[1:-1]
    return t


def t_IDENTIFIER(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = reserved.get(t.value, "IDENTIFIER")
    return t


# pylint: enable=C0103


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


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


def t_error(t):
    """
    Handles lexical errors. When a lexical error is encountered, prints an error
    message with line and column information and a marker pointing to the location
    of the error.
    """

    global _LEXER_DATA
    if not _LEXER_DATA:
        _LEXER_DATA = t.lexer.lexdata
    line = t.lexer.lineno
    pos = t.lexer.lexpos
    col = _find_column(_LEXER_DATA, pos)

    start = _LEXER_DATA.rfind("\n", 0, pos) + 1
    end = _LEXER_DATA.find("\n", pos)
    if end < 0:
        end = len(_LEXER_DATA)
    err_line = _LEXER_DATA[start:end]

    marker = " " * (col - 1) + "^"
    print(
        f"Lexical error at line {line}, column {col}: unexpected character '{t.value[0]}'"
    )
    print(err_line)
    print(marker)
    t.lexer.skip(1)


def build_lexer(input_data=None, **kwargs):
    """
    Build and return a lexer. Optionally initialize with input_data (string) for improved errors.
    """
    global _LEXER_DATA
    _LEXER_DATA = input_data or ""
    lex_obj = lex.lex(**kwargs)
    if input_data is not None:
        lex_obj.input(input_data)
    return lex_obj


lexer = build_lexer()
