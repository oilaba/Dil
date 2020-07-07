from ast import literal_eval
from api import builtins, loadmodule
import sys
##import operator

def reset():
    global modules, stack, current_scope, scopes, points
    modules = {}
    stack = []
    current_scope = None
    scopes = []
    points = [0]

modules = {}
##default(modules)

stack = []
current_scope = None
scopes = []
points = [0]

debug = 1
if debug:
    debug_scopes = lambda: print(scopes)
    debug_stack = lambda: print(stack)
    debug_module = lambda: print(modules)
    debug_points = lambda: print(points)

    builtins["scopes"] = debug_scopes
    builtins["stack"] = debug_stack
    builtins["modules"] = debug_module
    builtins["points"] = debug_points

commands = {}

def command(f):
    commands[f.__name__] = f
    return f

@command
def loadname(name):
    try:
        stack.append(current_scope[name])
    except KeyError:
        try:
            stack.append(scopes[0][name]) # globals
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
def cmp(a):
    if a == "==":
        s = stack.pop() == stack.pop()
    elif a == ">":
        s = stack.pop() > stack.pop()
    elif a == "<":
        s = stack.pop() < stack.pop()
    elif a == "!=":
        s = stack.pop() != stack.pop()
    stack.append(s)

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

@command
def pop():
    stack.pop()

@command
def use(module_name):
    try:
        m = modules[module_name]
    except:
        m = loadmodule(module_name)
        modules[module_name] = m
    current_scope[module_name] = m
        

@command
def useall(module_name):
    try:
        m = modules[module_name]
    except:
        m = loadmodule(module_name)
        modules[module_name] = m
    current_scope.update(m)

@command
def jump(n):
    points[-1] = int(n) -1

@command
def jumpif(n):
    e = stack.pop()
    assert type(e) == bool
    if e:
        points[-1] = int(n) -1

@command
def jumpnif(n):
    e = stack.pop()
    assert type(e) == bool
    if not e:
        points[-1] = int(n) -1
##########


def exec_line(line):
    try:
        c, f = line
    except ValueError:
        c = line[0]
        commands[c]()
        return
    commands[c](f)

def exec_code(code):
    code = optimize_code(code)
    while True:
        try:
            c = code[points[-1]]
        except IndexError:
##            input("[Program Finished]")
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




