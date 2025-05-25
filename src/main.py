"""Main module."""

from common.interpreter import Interpreter
from common.parser import parse


def run_file(path):
    """Runs a given My-Lang file.

    :param path: The path to the My-Lang file to run.
    """
    with open(path, encoding="utf-8") as f:
        code = f.read()
    ast = parse(code)
    Interpreter().visit(ast)


def repl():
    """Runs an interactive My-Lang shell.

    This function runs an infinite loop in which it reads a line of input from
    the user, parses it as a My-Lang program, and runs it. The result of the
    program is printed to the console. If the user enters a line with no content,
    the loop continues immediately. If the user enters an invalid program, the
    error is printed to the console. The loop can be broken by entering EOF
    (usually by pressing Ctrl+D in the terminal).
    """
    interp = Interpreter()
    while True:
        try:
            line = input(">>> ")
            if not line.strip():
                continue
            ast = parse(line)
            result = interp.visit(ast)
            if result is not None:
                print(result)
        except EOFError:
            print("Saindo.")
            break
        except Exception as e:
            print(f"[Error] {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()
