from ast import literal_eval
from api import default, builtins
import sys
##import operator

modules = {}
default(modules)

stack = []
current_scope = None
scopes = []
points = [0]

debug_scopes = lambda: print(scopes)
debug_stack = lambda: print(stack)

builtins["scopes"] = debug_scopes
builtins["stack"] = debug_stack

commands = {}

def command(f):
    commands[f.__name__] = f
    return f

@command
def loadname(name):
    try:
        stack.append(current_scope[name])
    except KeyError:
        stack.append(builtins[name])

@command
def storename(name):
    current_scope[name] = stack.pop()

@command
def loadconst(const):
    stack.append(literal_eval(const))

@command
def call(n):
    stack.append(stack.pop()(*(stack.pop() for i in range(int(n)))))


@command
def op(a):
    if a == "add":
        s = stack.pop() + stack.pop()
    elif a == "sub":
        s = stack.pop() - stack.pop()
    elif a == "mul":
        s = stack.pop() * stack.pop()
    elif a == "div":
        s = stack.pop() / stack.pop()
    stack.append(s)

@command
def scope(n):
    global current_scope
    n = int(n)
    if n < 0:
        for i in range(-n):
            scopes.pop()
        try:
            current_scope = scopes[-1]
        except IndexError:
            current_scope = None
    else:
        for i in range(n):
            scopes.append({})
        current_scope = scopes[-1]


##########


def exec_line(line):
    c, f = line
    commands[c](f)

def exec_code(code):
    code = optimize_code(code)
    while True:
        try:
            c = code[points[-1]]
        except IndexError:
            input("[Program Finished]")
            break
        exec_line(c)
        points[-1] += 1



def optimize_code(code):
    code = code.split("\n")
    r = []
    for line in code:
        s = tuple(line.split(" ", 1))
        if s[0]:
            r.append(s)
    return r

if __name__ == "__main__":   
    file = "asm.txt" # sys.argv[1]

    with open(file, encoding = "utf-8") as f:
        code = f.read()

    exec_code(code)




