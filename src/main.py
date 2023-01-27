from ply.lex import lex
from ply.yacc import yacc

tokens = (
    # 'real' is commented
    'PROGRAM', 'VAR', 'INTEGER', 'BEGIN', 'END', 'IF', 'THEN', 'ELSE', 'WHILE', 'PRINT',
    'AND', 'OR',
    'MOD', 'NOT', 'ASSIGN', 'PLUS', 'MINUS', 'MULT', 'DIVIDE', 'GT', 'LT', 'EQ', 'NEQ', 'GTEQ', 'LTEQ',
    'IDENTIFIER', 'SEMICOLON', 'COLON', 'COMMA', 'LPAREN', 'RPAREN', 'DO')

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_PROGRAM = r'program'
t_VAR = r'var'
t_INTEGER = r'integer'
# t_REAL = r'real'
t_BEGIN = r'begin'
t_END = r'end'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_WHILE = r'while'
t_PRINT = r'print'
t_AND = r'and'
t_OR = r'or'
t_MOD = r'mod'
t_NOT = r'not'
t_DO = r'do'
t_ASSIGN = r'[:]{1}[=]{1}'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIVIDE = r'\/'
t_GT = r'\>'
t_LT = r'\<'
t_EQ = r'\='
t_NEQ = r'[<]{1}[>]{1}'
t_GTEQ = r'[>]{1}[=]{1}'
t_LTEQ = r'[<]{1}[=]{1}'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_LPAREN = r'\('
t_RPAREN = r'\)'


# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

temp_counter = 0
def new_temp():
    global temp_counter
    temp_counter += 1
    return f"T_{temp_counter}"



# Build the lexer object
lexer = lex()

precedence = (
    ('right', 'OR'),
    ('right', 'AND'),
    ('right', 'PLUS', 'MINUS'),
    ('right', 'MULT', 'DIVIDE', 'MOD'),
    ('right', 'UNOT'),
    ('right', 'UMINUS'),
)

class Quadruple:
    def __init__(self, op, left, right, result):
        self.op = op
        self.left = left
        self.right = right
        self.result = result


quadruples = []
symbol_table = {}


def backpatch(quad_list, label):
    for i in quad_list:
        quadruples[i].result = label

def nextinstr():
    return len(quadruples) + 1


class E:
    def __init__(self, t, f):
        self.trueList = t
        self.falseList = f

def p_marker(t):
    'marker : '
    t[0] = nextinstr()

def p_endmarker(t):
    'endmarker : '
    nextList = [nextinstr()]
    t[0] = {'next': nextList}
    quadruples.append(Quadruple('GOTO', None, None, None))
    


def p_program(t):
    'program : PROGRAM IDENTIFIER declarations compoundstatement'
    pass
    print('shit', t[1])

def p_declarations(t):
    '''declarations : VAR declarationlist 
                    | empty
    '''
    pass

def p_empty(p):
     'empty :'
     pass

def p_declarationlist(t):
    '''
    declarationlist : identifierlist COLON type
                    | declarationlist SEMICOLON identifierlist COLON type
    '''
    pass

def p_identifierlist(t):
    '''
    identifierlist : IDENTIFIER
                   | identifierlist COMMA IDENTIFIER 
    '''

def p_type(t):
    # for know we support only int
    'type : INTEGER'
    pass

def p_compoundstatement(t):
    'compoundstatement : BEGIN statementlist END'
    pass
    t[0] = Quadruple("begin_block", None, None, None)
    nextInstruction = nextinstr()
    backpatch(t[2].next, nextInstruction)
    t[0].next = t[2].next


def p_statementlist(t):
    '''statementlist : statement 
                     | statementlist SEMICOLON statement
    '''
    pass

def p_statement(t):
    '''
    statement : compoundstatement                           
              | PRINT LPAREN expression RPAREN              
    '''
    # TODO for know while statement is commented
            #   | WHILE expression DO statement               
     
    pass

def p_statement_assign(t):
    'statement : IDENTIFIER ASSIGN expression'
    result = t[1]
    quadruples.append(Quadruple("=", t[3].place, None, result))

    t[0] = {'place': result, 'trueList': [], 'falseList':[]}


def p_if_else_statement(t):
    'statement : IF expression THEN marker statement endmarker ELSE marker statement'
    backpatch(t[2]['trueList'], t[4])
    backpatch(t[2]['falseList'], t[8])
    nextList = t[5].next + t[6].next + t[9].next 
    t[0] = {'next': nextList}


def p_if_statement(t):
    'statement : IF expression THEN marker statement'
    # t[4] is newinstr
    backpatch(t[2]['trueList'], t[4])
    nextList = t[2].falseList + t[4].next
    t[0] = {'next': nextList }


def p_expression(t):
    '''
    expression : LPAREN expression RPAREN
    '''
    trueList = t[2].trueList
    falseList = t[2].falseList
    result = t[2].place
    t[0] = {'place': result, 'type':'expression', 'trueList': trueList, 'falseList': falseList}


def p_expression_int(t):
    '''
    expression : INTEGER
               | IDENTIFIER
    '''
    # generate backpatching code
    result = new_temp()
    quadruples.append(Quadruple('=', t[1], None, result))
    trueList = []
    falseList = []

    t[0] = {'place': result, 'type': 'expression', 'trueList': trueList, 'falseList': falseList}

def p_expression_plus(t):
    '''
    expression : expression PLUS expression    
    '''
    result = new_temp()
    quadruples.append(Quadruple('+', t[1]['place'], t[3]['place'], result))
    t[0] = {'place': result, 'type': 'expression', 'trueList': [], 'falseList': []}

def p_expression_minus(t):
    '''
    expression : expression MINUS expression    
    '''
    result = new_temp()
    quadruples.append(Quadruple('-', t[1]['place'], t[3]['place'], result))
    t[0] = {'place': result, 'type': 'expression', 'trueList': [], 'falseList': []}

def p_expression_mult(t):
    '''
    expression : expression MULT expression    
    '''
    result = new_temp()
    quadruples.append(Quadruple('*', t[1]['place'], t[3]['place'], result))
    t[0] = {'place': result, 'type': 'expression', 'trueList': [], 'falseList': []}

def p_expression_divide(t):
    '''
    expression : expression DIVIDE expression    
    '''
    result = new_temp()
    quadruples.append(Quadruple('/', t[1]['place'], t[3]['place'], result))
    t[0] = {'place': result, 'type': 'expression', 'trueList': [], 'falseList': []}

def p_expression_mod(t):
    '''
    expression : expression MOD expression    
    '''
    result = new_temp()
    quadruples.append(Quadruple('%', t[1]['place'], t[3]['place'], result))
    t[0] = {'place': result, 'type': 'expression', 'trueList': [], 'falseList': []}


def p_expression_and(t):
    '''
    expression : expression AND expression     
    '''
    # t[3] is nextinstruction line
    # there is no need to marker since
    # we can calling nextintr func directly
    result = new_temp()
    quadruples.append(Quadruple('&&', t[1]['place'], t[3]['place'], result))

    backpatch(t[1].trueList, nextinstr())
    trueList = t[4].trueList
    falseList = t[1].falseList + t[4].falseList

    t[0] = {'place': result, 'type': 'expression', 'trueList': trueList, 'falseList': falseList}

def p_expression_or(t):
    '''
    expression : expression OR expression     
    '''
    # t[3] is nextinstruction line
    # there is no need to marker since
    # we can calling nextintr func directly
    result = new_temp()
    quadruples.append(Quadruple('||', t[1]['place'], t[3]['place'], result))

    backpatch(t[1].falseList, nextinstr())
    trueList = t[1].trueList + t[4].trueList
    falseList = t[4].falseList

    t[0] = {'place': result, 'type': 'expression', 'trueList': trueList, 'falseList': falseList}


# def p_expression_or(t):
#     '''
#     expression : expression OR marker expression     
#     '''
#     # t[3] is nextinstruction line
#     backpatch(t[1].falseList, t[3])
#     trueList = t[1].trueList + t[4].trueList
#     falseList = t[4].falseList

#     t[0] = E(trueList, falseList)

def p_expression_not(t):
    '''
    expression : NOT expression %prec UNOT
    '''
    result = new_temp()
    quadruples.append(Quadruple('!', t[2]['place'], None, result))

    trueList = t[2].trueList
    falseList = t[2].falseList
    return {'place':result, 'type': 'expression', 'trueList': falseList, 'falseList': trueList}

def expression_relop(t):
    '''
    expression : expression LT expression      
               | expression EQ expression      
               | expression GT expression      
               | expression NEQ expression     
               | expression LTEQ expression    
               | expression GTEQ expression         
    '''
    nextInstruction = nextinstr() 
    trueList = [nextInstruction]
    falseList = [nextInstruction+1]

    quadruples.append(Quadruple(f'if {t[1].place} {t[2]} {t[3].place} GOTO', None, None, None))
    quadruples.append(Quadruple(f'GOTO', None, None, None))

    return {'type': 'expression', 'trueList': trueList, 'falseList': falseList}



def p_expression_minus(t):
    '''
    expression : MINUS expression %prec UMINUS 
    '''
    result = new_temp()
    quadruples.append(Quadruple('-', '0', t[2]['place'], result))
    t[0] = {'place': result, 'type': 'expression', 'trueList': [], 'falseList': []}



# Build the parser
parser = yacc(start="program")

# Parse an expression

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    r = parser.parse(s)
    print(quadruples)
    print(r.trueList, r.falseList)
    quadruples.clear()
    