import operator
from func import func
from call import call
from primop import primop
from errors import exponentiationError

opList = ["+", "*", "^", "@", "!", "="]

ops_mapping = {
    "+": func(["k", "x", "y"],
              call("k", [call("+", ["x", "y"])])),
    "*": func(["k", "x", "y"],
              call("k", [call("*", ["x", "y"])])),
    "^": func(["k", "x", "y"],
              call("k", [call("^", ["x", "y"])])),
    "@": func(["k", "x"],
              call("k", [call("@", ["x"])])),
    "!": func(["k", "x"],
              call("k", [call("!", ["x"])])),
    "=": func(["k", "x", "y"],
              call("k", [call("=", ["x", "y"])])),
}

"""
    Below are the arithmetic/memory functions that evaluate prim-ops
    All of them take in an Array of arguments and return the operation
    applied to the arguments (The final argument is always a Store)
"""
def plus_op(a):
    return operator.add(*a[:2]), a[2]
def mult_op(a):
    return operator.mul(*a[:2]), a[2]

def exponent(args):
    if args[1] >= 0:
        return operator.pow(*args[:2]), args[2]
    else:
        raise exponentiationError()

def at_op(a):
    return a[1].alloc_generated(a[0]), a[1]

def bang_op(a):
    return a[1].getAt(a[0].loc), a[1]

def eq_op(a):
    return a[2].setAt(a[0], a[1]), a[2]

#
ops = [("+", primop("+", plus_op, 3)),
       ("*", primop("*", mult_op, 3)),
       ("^", primop("^", exponent, 3)),
       ("@", primop("@", at_op, 2)),
       ("!", primop("!", bang_op, 2)),
       ("=", primop("=", eq_op, 3))]


