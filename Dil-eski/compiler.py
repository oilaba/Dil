from ast import literal_eval
import operator

operantor_dict = {"+": operator.add,
                  "-": operator.sub,
                  "/": operator.truediv,
                  "*": operator.mul,
                  "<": operator.lt,
                  ">": operator.gt,
                  "==": operator.eq,
                  "!=": operator.ne,}

tokens = [
    "NAME",
    "EQUAL",
    "STRING",
    "LPAREN",
    "RPAREN",
    "NUMBER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "FLOAT",
    "IF",
    "THEN",
    "ELSE",
    "WHILE",
    "IMPORT",
    "IMPORTALL",
    #cmp
    "EQ",
    "LT",
    "GT",
    "NE",
    ]

t_NAME = r"\w[\w0-9_]*"
t_EQUAL = r"="

t_LPAREN  = r'\('
t_RPAREN  = r'\)'

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'

t_EQ = r"=="
t_LT = r"<"
t_GT = r">"
t_NE = r"!="

t_ignore = " \t"

literals = ",{};"

def t_IF(t): r'eğer'; return t
def t_THEN(t): r'ise'; return t
def t_ELSE(t): r'değilse'; return t

def t_WHILE(t): r'iken'; return t

def t_IMPORT(t): r'kullan:'; return t
def t_IMPORTALL(t): r'aktar:'; return t

def t_FLOAT(t):
    r'[-+]\d+\.\d*|\d+\.\d*'
##    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'[-+]\d+|\d+'
##    t.value = int(t.value)
    return t

def t_STRING(t):
    r'''(".*?") | ('.*?')'''
##    t.value = literal_eval(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    global e
    e = t
    print(f"Illegal character {t.value[0]!r} at {t.lineno}:{t.lexpos}")



### lexer done!
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'EQ', 'NE', 'LT', 'GT')
    )

start = "statements"

def p_scope(p):
    "scope : '{' statements '}'"
    p[0] = ("scope", p[2])

def p_empty_scope(p):
    "scope : '{' '}'"
    p[0] = ("scope", None)

##def p_empty_statement(p):
##    "statement :"
##    p[0] = None

def p_statements(p):
    "statements : statements statement"
    p[0] = p[1] + (p[2],)

def p_statements_last(p):
    "statements : statement"
    p[0] = p[1],

def p_statement(p):
    """statement : scope
                 | var_assign
                 | compound_expr
                 | import_stmt"""
    p[0] = p[1]

def p_import_stmt(p):
    """import_stmt : IMPORT names"""
    p[0] = ("use", p[2])

def p_importall_stmt(p):
    """import_stmt : IMPORTALL names"""
    p[0] = ("useall", p[2])

def p_names(p):
    "names : names ',' NAME"
    p[0] = (p[3],) + p[1]

def p_names_last(p):
    "names : NAME"
    p[0] = p[1],

def p_statement_pop(p):
    """statement : eval_expr"""
    p[0] = ("pop", p[1])

def p_var_assign(p):
    """var_assign : NAME EQUAL eval_expr"""
    p[0] = ("assign", p[1], p[3])

def p_args(p):
    "args : args ',' eval_expr"
    p[0] = (p[3],) + p[1]

def p_args_last(p):
    "args : eval_expr"
    p[0] = p[1],

def p_eval_expr_paren(p):
    "eval_expr : LPAREN eval_expr RPAREN"
    p[0] = p[2]
    
def p_eval_expr(p):
    """eval_expr : var
                 | const
                 | func_call
                 | compare_expr"""
    p[0] = p[1]

def p_eval_op_expr(p):
    """eval_expr : eval_expr TIMES eval_expr
                 | eval_expr DIVIDE eval_expr
                 | eval_expr PLUS eval_expr
                 | eval_expr MINUS eval_expr"""
    f, s = p[1], p[3]
    if f[0] == s[0] == "const":
        p[0] = ("const", str(operantor_dict[p[2]](literal_eval(f[1]), literal_eval(s[1]))))
    else:
        p[0] = ("op", p[2], s, f)

##def p_operand(p):
##    """operand : TIMES
##               | DIVIDE
##               | PLUS
##               | MINUS"""
##    p[0] = p[1]

def p_const(p):
    """const : NUMBER
             | STRING
             | FLOAT"""
    p[0] = ("const", p[1])

def p_var(p):
    """var : NAME"""
    p[0] = ("var", p[1])

def p_func_call(p):
    """func_call : eval_expr LPAREN RPAREN"""
    p[0] = ("call", p[1])

def p_arg_func_call(p):
    """func_call : eval_expr LPAREN args RPAREN"""
    p[0] = ("argcall", p[1], p[3])

def p_compound_expr(p):
    """compound_expr : if_stmt
                     | while_stmt"""
    p[0] = p[1]

def p_if_stmt(p):
    """if_stmt : IF eval_expr THEN scope"""
    p[0] = ("ifstmt", p[2], p[4])
    
def p_ifelse_stmt(p):
    """if_stmt : IF eval_expr THEN scope ELSE scope"""
    p[0] = ("ifelse", p[2], p[4], p[6])

def p_while(p):
    """while_stmt : eval_expr WHILE scope"""
    p[0] = ("while", p[1], p[3])

def p_compare(p):
    """compare_expr : eval_expr EQ eval_expr
                    | eval_expr NE eval_expr
                    | eval_expr GT eval_expr
                    | eval_expr LT eval_expr"""
    p[0] = ("cmp", p[2], p[3], p[1])

def p_error(p):
    global e
    e=p
    print("Error", p.value, p.type, p.lineno, p.lexpos)
    

### parser done!
    

import ply.lex as lex
lex.lex()
import ply.yacc as yacc
yacc.yacc()


def run(file):
    global ast, asm
    
    with open(file, encoding = "utf-8") as f:
        code = f.read()

    ast = yacc.parse(code)
    ast = ("scope", ast)

    from astcompiler import walk_node
    asm = walk_node(ast)

    with open("asm.txt", "w", encoding = "utf-8") as f:
        f.write(asm)

    from interpreter import exec_code, reset
    reset()
    exec_code(asm)

def execute(asm):
    from interpreter import exec_code, reset
    reset()
    exec_code(asm)

def comp(file):
    with open(file, encoding = "utf-8") as f:
        code = f.read()

    ast = yacc.parse(code)
    ast = ("scope", ast)

    from astcompiler import walk_node
    asm = walk_node(ast)
    return asm

if __name__ == "__main__":
    run("kod.txt")
    input()


from dis import dis
if 0:
    dis(r"""isim = oku("Merhaba! Adın ne?\n > ")
    u = uzunluk(isim)
    if u < 4:
            yaz("Adın çok kısa.")

    if 4 < u < 8 :
            yaz("Adın normal.")

    if u > 8 :
            yaz("Adın çok uzun.")
    """)
