operands = {"+":"add", "-":"sub", "/":"div", "*":"mul"}

line_number = 0

nodes = {}
def node(f):
    nodes[f.__name__] = f
    return f

def walk_node(ast):
    node, *elements = ast
    s = nodes[node](*elements)
    return s

@node
def scope(e):
    global line_number
    line_number += 1
    if not e: return ""
    s = "scope 1\n"
    for i in e:
        s += walk_node(i)
    line_number += 1
    return s + "scope -1\n"

@node
def pop(e):
    global line_number
    r = walk_node(e) + "pop\n"
    line_number += 1
    return r

@node
def use(e):
    global line_number
    s = ""
    for i in e:
        s += "use " + i + "\n"
        line_number += 1
    return s

@node
def useall(e):
    global line_number
    s = ""
    for i in e:
        s += "useall " + i + "\n"
        line_number += 1
    return s

@node
def assign(name, expr):
    global line_number
    r = walk_node(expr) + "storename " + name + "\n"
    line_number += 1
    return r

@node
def op(operand, a, b):
    global line_number
    r = walk_node(a) + walk_node(b) + "op " + operands[operand] + "\n"
    line_number += 1
    return r

@node
def const(c):
    global line_number
    line_number += 1
    return "loadconst " + c + "\n"

@node
def var(n):
    global line_number
    line_number += 1
    return "loadname " + n + "\n"

@node
def call(expr):
    global line_number
    r = walk_node(expr) + "call 0\n"
    line_number += 1
    return r

@node
def argcall(expr, args):
    global line_number
    s = ""
    for i in args:
        s += walk_node(i)
    r = s + walk_node(expr) + "call " + str(len(args)) + "\n"
    line_number += 1
    return r

@node
def cmp(t, l, r):
    global line_number
    r = walk_node(l) + walk_node(r) + "cmp " + t + "\n"
    line_number += 1
    return r

@node
def ifstmt(eval_expr, scope):
    global line_number
    condition = walk_node(eval_expr)
    line_number += 1
    s = walk_node(scope)
    return condition + "jumpnif " + str(line_number) + "\n" + s

@node
def ifelse(eval_expr, if_scope, else_scope):
    global line_number
    condition = walk_node(eval_expr)
    line_number += 1
    if_s = walk_node(if_scope)
    line_number += 1
    tail_of_if = line_number
    else_s = walk_node(else_scope)
    jump_to_else = "jumpnif " + str(tail_of_if) + "\n"
    pass_else = "jump " + str(line_number) + "\n"
    return condition + jump_to_else + if_s + pass_else + else_s

def main(ast):
    return walk_node(ast)








