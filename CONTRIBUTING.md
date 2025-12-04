# Contributing to BPL

Thank you for your interest in contributing to the Bangla Programming Language (BPL)! We welcome contributions of all kinds, from code improvements to documentation translations.

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Git
- Basic familiarity with Bangla language (not required for code contributions)

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/bpl.git
   cd bpl
   ```

3. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a new branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Making Changes

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and modules
- Keep functions small and focused

### Testing
Before submitting changes, run the test suite:

```bash
pytest tests/ -v
```

If adding new features, please add corresponding tests in the `tests/` directory.

### Commit Messages
Write clear, descriptive commit messages:
```bash
git commit -m "Add support for list data type

- Implement list literals [1, 2, 3]
- Add indexing operator []
- Add built-in len() function for lists"
```

## Types of Contributions

### 🐛 Bug Reports
Found a bug? Great! Please:
1. Open an issue with a clear title
2. Describe the problem and steps to reproduce
3. Include error messages and your environment info
4. Provide a minimal code example

Example:
```
Title: Factorial function throws error with negative numbers

Reproduction:
```bangla
দেখাও(factorial(-5))
```

Error: SyntaxError: ...
```

### ✨ Feature Requests
Have an idea? Let's discuss it:
1. Open an issue with `[FEATURE]` in the title
2. Describe the feature and why it's useful
3. Show example usage if possible
4. Note priority: High/Medium/Low

### 💻 Code Contributions

**Good first issues** for beginners:
- [ ] Add more built-in functions (abs, max, min, etc.)
- [ ] Improve error messages with line/column info
- [ ] Add string methods (upper, lower, length)
- [ ] Write documentation improvements

**For experienced contributors:**
- [ ] Implement list and dictionary types
- [ ] Build C transpiler backend
- [ ] Create IDE extensions (VS Code, etc.)
- [ ] Implement module/import system

### 📚 Documentation
Help improve our docs:
- Fix typos and clarify explanations
- Add more examples
- Translate documentation to other languages
- Write tutorials for beginners

### 🌐 Translation
Help make BPL accessible worldwide:
- Translate error messages to other languages
- Translate documentation
- Add examples in different languages

## Pull Request Process

1. **Update your fork** with latest changes:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request** on GitHub with:
   - Clear title describing changes
   - Description of what was changed and why
   - References to any related issues (`Fixes #123`)
   - Test results showing all tests pass

4. **Code Review**: 
   - Address feedback from reviewers
   - Make requested changes
   - Push updates to the same branch (PR updates automatically)

5. **Merge**: Once approved, your PR will be merged to main!

## Project Structure

Understanding the project layout:

```
bpl/
├── bangla_lang/              # Core interpreter
│   ├── lexer.py             # Tokenizer
│   ├── parser.py            # Parser (tokens → AST)
│   ├── ast.py               # AST node definitions
│   ├── evaluator.py         # Executor (AST → result)
│   ├── runtime.py           # Built-in functions
│   ├── cli.py               # Command-line interface
│   ├── repl.py              # Interactive shell
│   ├── tokens.py            # Token constants
│   ├── errors.py            # Error types
│   ├── utils.py             # Utilities
│   ├── unicode_variants.py  # Keyboard variant support
│   └── transpile/           # C backend (future)
├── examples/                 # Example programs (.bpl files)
├── tests/                    # Test suite
├── README.md                # Main documentation
├── pyproject.toml           # Project metadata
└── requirements.txt         # Dependencies
```

## Component Responsibilities

### Lexer (`lexer.py`)
- Converts raw source code into tokens
- Handles indentation (INDENT/DEDENT)
- Supports Bangla and Latin identifiers
- Normalizes Unicode variants

### Parser (`parser.py`)
- Converts tokens into Abstract Syntax Tree (AST)
- Implements recursive-descent parsing with precedence climbing
- Validates syntax rules

### AST (`ast.py`)
- Defines all AST node types
- Each node has position tracking (lineno, col)

### Evaluator (`evaluator.py`)
- Walks the AST and executes it
- Manages scopes (Environment class)
- Handles function calls and closures

### Runtime (`runtime.py`)
- Implements built-in functions (দেখাও, প্রকার, etc.)
- Available to all programs

## Testing Guidelines

Write tests that:
- Have clear, descriptive names
- Test one thing per test
- Include both positive and negative cases
- Follow the existing test structure

Example test:

```python
def test_function_definition_and_call():
    """Test defining and calling a simple function."""
    code = """
ফাংশন add(a, b):
  ফলাফল a + b

দেখাও(add(2, 3))
"""
    # Expected: prints 5
    result = evaluate(code)
    assert result == 5
```

## Debugging

### Enable Debug Output
```python
import sys
from bangla_lang.lexer import Lexer
from bangla_lang.parser import Parser

code = "দেখাও('হ্যালো')"
lexer = Lexer(code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)  # See token stream

parser = Parser(tokens)
ast = parser.parse()
print(ast)  # See AST structure
```

### Common Issues

**Issue**: Parser error on valid code  
**Debug**: Check that lexer is producing correct tokens

**Issue**: Runtime error  
**Debug**: Check evaluator's Environment and function scoping

**Issue**: Keyboard variant not recognized  
**Debug**: Add to `KEYWORD_VARIANTS` in `unicode_variants.py`

## Communication

- **Issues**: Use GitHub Issues for bugs and features
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Feedback**: Be respectful and constructive

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

- Check existing issues and pull requests
- Read the main README
- Open a discussion on GitHub

**Thank you for contributing to BPL! 🙏**

---

**Happy coding! কোড করুন আপনার ভাষায়! 🚀**
