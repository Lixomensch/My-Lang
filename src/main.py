from common.parser import parse
from common.interpreter import Interpreter

def run_file(path):
    with open(path, encoding='utf-8') as f:
        code = f.read()
    ast = parse(code)
    Interpreter().visit(ast)

def repl():
    interp = Interpreter()
    while True:
        try:
            line = input('>>> ')
            if not line.strip():
                continue
            ast = parse(line)
            result = interp.visit(ast)
            if result is not None:
                print(result)
        except EOFError:
            print('Saindo.')
            break
        except Exception as e:
            print(f'[Error] {e}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()
