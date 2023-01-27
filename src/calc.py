# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

tokens = (
    'TRUE','FALSE',
    'AND', 'OR', 'NOT',
    'LPAREN','RPAREN',
    )

# Tokens
t_OR = r'or'
t_AND = r'and'
t_NOT = r'not'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_TRUE = r'true'
t_FALSE = r'false'

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','OR'),
    ('left','AND'),
    ('right','UNOT'),
    )

# dictionary of names
names = { }

quadruples = []

def backpatch(l: list, i: int):
    for line_number in l:
        quadruples[line_number - 1] = ("goto", i)

def nextinstr():
    return len(quadruples) + 1

def p_marker(t):
    'marker : '
    t[0] = nextinstr()

class E:
    def __init__(self, t, f):
        self.truelist = t
        self.falselist = f

def p_expression_or(t):
    '''expression : expression OR marker expression'''
    backpatch(t[1].falselist, t[3])
    truelist = t[1].truelist + t[4].truelist
    falselist = t[4].falselist
    t[0] = E(truelist, falselist)

def p_expression_and(t):
    'expression : expression AND marker expression'
    backpatch(t[1].truelist, t[3])
    truelist = t[4].truelist
    falselist = t[4].falselist + t[1].falselist
    t[0] = E(truelist, falselist)

def p_expression_unot(t):
    'expression : NOT expression %prec UNOT'
    t[0] = E(t[2].falselist, t[2].truelist)

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_true(t):
    'expression : TRUE'
    t[0] = E([nextinstr()], [])
    quadruples.append(("goto", ))

def p_expression_false(t):
    'expression : FALSE'
    t[0] = E([], [nextinstr()])
    quadruples.append(("goto", ))

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc(start="expression")

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    r = parser.parse(s)
    print(quadruples)
    print(r.truelist, r.falselist)
    quadruples.clear()
    