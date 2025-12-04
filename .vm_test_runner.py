from bangla_lang.lexer import Lexer
from bangla_lang.parser import Parser
from bangla_lang.compiler import Compiler
from bangla_lang.bytecode import VM
from bangla_lang import runtime
from bangla_lang.unicode_variants import get_canonical_keyword, is_keyword_variant
from bangla_lang.unicode_variants import normalize_bangla_keyword, KEYWORD_VARIANTS

src = 'ফাংশন add(a, b):\n  ফলাফল a + b\n\nদেখাও(add(2, 3))\n'
print('SOURCE:\n', src)
print("canonical('ফাংশন'):", get_canonical_keyword('ফাংশন'), "is_variant:", is_keyword_variant('ফাংশন'))
print("canonical('ফংশন'):", get_canonical_keyword('ফংশন'), "is_variant:", is_keyword_variant('ফংশন'))
print("canonical('দেখাও'):", get_canonical_keyword('দেখাও'), "is_variant:", is_keyword_variant('দেখাও'))
print("normalize('ফাংশন') repr:", repr(normalize_bangla_keyword('ফাংশন')))
print('Keyword variant keys sample:', list(KEYWORD_VARIANTS.keys())[:20])

lex = Lexer(src)
tokens = lex.tokenize()
print('TOKENS:', [ (t.type, t.value) for t in tokens[:20] ])
parser = Parser(tokens)
ast = parser.parse()
print('AST type:', type(ast).__name__)
comp = Compiler()
codeobj = comp.compile(ast)
print('Compiled constants count:', len(codeobj.consts))
print('Names:', codeobj.names)
print('Instructions:')
for i, ins in enumerate(codeobj.instructions):
    print(i, ins)

vm = VM()
res = vm.run_code(codeobj, globals_={})
print('VM returned:', res)
