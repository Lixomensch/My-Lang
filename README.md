```markdown
# My-Lang

Uma linguagem de programação customizada implementada em Python usando PLY (lex & yacc). Ela suporta:

- **Tipos de dados**  
  - Números (inteiros e ponto-flutuante)  
  - Texto (strings)  
  - Booleanos literais (`true` / `false`)  
- **Expressões**  
  - Aritméticas (`+`, `-`, `*`, `/`)  
  - Relacionais (`==`, `!=`, `<`, `<=`, `>`, `>=`)  
  - Lógicas (`and`, `or`, `not`)  
  - Concatenação de strings via `+`  
- **Variáveis** com escopo léxico  
- **Estruturas condicionais**: `if (…) { … } else { … }`  
- **Estruturas de repetição**: `while (…) { … }`  
- **Entrada e saída**:  
  - `print(expr);`  
  - `input("prompt")` tanto como expressão quanto statement  
- **Funções**: declaração com `func nome(par1, par2…) { … }` e chamada `nome(arg1, arg2…);`

---

## Estrutura do Projeto

```

My-Lang/
├── src/
│   ├── common/
│   │   ├── lexer.py         # definição de tokens e tratamento de erros lexicais
│   │   ├── ast\_nodes.py     # classes AST (números, strings, variáveis, ops, controle, funções)
│   │   ├── parser.py        # grammar rules, LALR parser, erros sintáticos detalhados
│   │   └── interpreter.py   # Environment & Interpreter, dispatch visit\_\*, escopo, built-ins
│   ├── main.py              # runner de arquivo ou modo REPL interativo
│   └── repl.py              # REPL standalone (pode invocar diretamente)
├── test/
│   ├── test\_program.mylang  # programa de exemplo simples
│   └── test\_program2.mylang # programa de teste abrangente
├── README.md                # este arquivo
└── requirements.txt         # dependências (PLY)

````

---

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/SeuUsuario/My-Lang.git
   cd My-Lang
````

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

   > **requirements.txt** deve conter ao menos:
   >
   > ```
   > ply>=3.11
   > ```

---

## Uso

### Rodar um arquivo `.mylang`

```bash
python src/main.py test/test_program.mylang
```

### Modo REPL interativo

```bash
python src/main.py
```

Exemplos de comandos no REPL:

```
>>> var x = 5;
>>> print(x * 2);
10
>>> func sum(a, b) { print(a + b); }
>>> sum(3, 4);
7
```

---

## Exemplos de Código

```mylang
// Programa Fibonacci simples
func fib(n) {
  if (n < 2) {
    return n;
  } else {
    return fib(n-1) + fib(n-2);
  }
}

var num = input("Digite um inteiro: ");
print("Fib(" + num + ") = " + fib(num));
```

---

## Testes

Os dois programas em `test/` cobrem todas as funcionalidades:

* **test\_program.mylang**: casos básicos (tipos, expressões, if, while, funções simples).
* **test\_program2.mylang**: casos avançados (escopo, loops aninhados, booleanos, side-effects).

Para executá-los, use:

```bash
python src/main.py test/test_program2.mylang
```

---

## Contribuição

1. Abra uma *issue* descrevendo sua sugestão ou correção.
2. Faça um *fork* e crie uma *branch feature/x*.
3. Implemente e teste suas mudanças.
4. Envie um *pull request* detalhando o que foi alterado.

---

## Licença

MIT © \[Seu Nome]

```
```
