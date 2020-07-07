import ply.lex as lex
import ply.yacc as yacc
from decimal import Decimal

class Calc():

    def __init__(self, is_perfect = False):
        self.lexer = lex.lex(module = self)
        self.parser = yacc.yacc(module = self)
        self.is_perfect = is_perfect
        if self.is_perfect:
            self.int = Decimal
            self.float = Decimal
        else:
            self.int = int
            self.float = float

    # lexer

    tokens = (
        'NUMBER',
        'FLOAT',
        'PLUS',
        'MINUS',
        'EXP',
        'TIMES',
        'DIVIDE', 
        'LPAREN',
        'RPAREN',
        'INTDIV',
        'MODULO',
    )

    # Tokens

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_EXP = r'\*\*'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_INTDIV = r'//'
    t_MODULO = r'%'

    def t_FLOAT(self, t):
        r'\d+\.\d*'
        t.value = self.float(t.value)
        return t
    
    def t_NUMBER(self, t):
        r'\d+'
        t.value = self.int(t.value)
        return t

    t_ignore = " \t"

    def t_error(self, t):
        err = SyntaxError("Invalid character '{}' at index {}.".format(t.value, t.lexpos))
        err.info = t
        raise err
    
    # Parser

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'EXP'),
        ('right', "UMINUS", "UPLUS")
    )

    start = "expression"

    def p_statement_paren(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_add(self, p):
        """
        expression : expression PLUS expression"""
        p[0] = p[1] + p[3]

    def p_expression_sub(self, p):
        """
        expression : expression MINUS expression"""
        p[0] = p[1] - p[3]

    def p_expression_mult(self, p):
        """
        expression : expression TIMES expression"""
        p[0] = p[1] * p[3]

    def p_expression_div(self, p):
        """
        expression : expression DIVIDE expression"""
        p[0] = p[1] / p[3]

    def p_expression_pow(self, p):
        """
        expression : expression EXP expression"""
        p[0] = p[1] ** p[3]

    def p_expression_intdiv(self, p):
        """
        expression : expression INTDIV expression"""
        p[0] = p[1] // p[3]

    def p_expression_modulo(self, p):
        """
        expression : expression MODULO expression"""
        p[0] = p[1] % p[3]

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = -p[2]

    def p_expression_uplus(self, p):
        'expression : PLUS expression %prec UPLUS'
        p[0] = +p[2]

    def p_expression_number(self, p):
        """expression : NUMBER
                      | FLOAT"""
        p[0] = p[1]


    def p_error(self, p):
        if p:
            err = SyntaxError("Invalid '{}' ('{}') token at index {}.".format(p.type, p.value, p.lexpos))
            err.info = p
            raise err
        else:
            raise EOFError("Syntax error at EOF")


    def evaluate(self, string):
        return self.parser.parse(string, self.lexer)
    
    __call__ = evaluate # alias
    

if __name__ == '__main__':
    işlem = Calc(True)
    try:
        while True:
            print(işlem(input()))
    except SyntaxError as e:
        print("Hata:", e.info)
        raise
