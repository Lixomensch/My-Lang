# My-Lang

A custom programming language implemented in Python using PLY (lex & yacc). It supports:

* **Data Types**

  * Numbers (integers and floating-point)
  * Text (strings)
  * Boolean literals (`true` / `false`)
* **Expressions**

  * Arithmetic (`+`, `-`, `*`, `/`)
  * Relational (`==`, `!=`, `<`, `<=`, `>`, `>=`)
  * Logical (`and`, `or`, `not`)
  * String concatenation with `+`
* **Variables** with lexical scope
* **Conditional Structures**: `if (…) { … } else { … }`
* **Loop Constructs**: `while (…) { … }`
* **Input and Output**:

  * `print(expr);`
  * `input("prompt")` as both an expression and a statement
* **Functions**: declare with `func name(param1, param2…) { … }` and invoke with `name(arg1, arg2…);`

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/YourUser/My-Lang.git
   cd My-Lang
   ```

2. (Optional, but recommended) Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Linux/macOS
   .venv\Scripts\activate       # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   > **requirements.txt** should include at least:
   >
   > ```txt
   > ply>=3.11
   > ```

## Usage

### Running a `.mylang` file

```bash
python src/main.py test/test_program.mylang
```

### Interactive REPL Mode

```bash
python src/main.py
```

Examples in the REPL:

```mylang
>>> var x = 5;
>>> print(x * 2);
10
>>> func sum(a, b) { print(a + b); }
>>> sum(3, 4);
7
```

## Code Examples

```mylang
// Simple Fibonacci program
func fib(n) {
  if (n < 2) {
    return n;
  } else {
    return fib(n-1) + fib(n-2);
  }
}

var num = input("Enter an integer: ");
print("Fib(" + num + ") = " + fib(num));
```

## Tests

The two programs in `test/` cover all features:

* **test\_program.mylang**: basic cases (types, expressions, if, while, simple functions).
* **test\_program2.mylang**: advanced cases (scoping, nested loops, booleans, side-effects).

To run them:

```bash
python src/main.py test/test_program2.mylang
```

## License

This repository is licensed under the [MIT License](https://github.com/YourUser/My-Lang/blob/main/LICENSE).