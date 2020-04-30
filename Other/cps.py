from decl import decl
from func import func
from call import call
from cond import cond
from stop import stop
from grab import grab
from string import ascii_lowercase
from prelude import opList, ops_mapping
from declSequence import declSequence

COUNT = 0
FCOUNT = 0

# String, Integer -> String
# Creates a new variable, using k and some other letter
def new_var(var, x):
    count = x % 26
    return var + ascii_lowercase[count]

# ParsedToy -> ParsedToy (CPS Formatted)
# Takes in the ParsedToy expression and formats it into continuation passing format
# Handles special cases of declarations and their sequences, passes the rest to split
def receive(toy):
    global COUNT
    if type(toy) == decl:
        toy.rhs = value(toy.rhs)
        return toy
    elif type(toy) == declSequence:
        new_sequence = []
        for declaration in toy.sequence:
            new_sequence.append(receive(declaration))
        toy.sequence = new_sequence
        toy.expr = receive(toy.expr)
        return toy
    else:
        COUNT += 1
        return func(new_var("k", COUNT), split(toy, new_var("k", COUNT)))

# ParsedToy, String -> ParsedToy
# Splits the ParsedToy into the CPS format
# Takes each structure and turns it into its atomic bits, handling only a single
# piece of then 'toy' being evaluated at a single time
def split(toy, k):
    global COUNT
    if type(toy) == str:
        if toy in opList:
            return call(k, ops_mapping[toy])
        return call(k, toy)
    if type(toy) == int:
        return call(k, toy)
    if type(toy) == func:
        return call(k, value(toy))
    if type(toy) == call:
        return split_call(toy, k)
    if type(toy) == cond:
        conditional = cond("of-tst", split(toy.true_expression, k), split(toy.false_expression, k))
        f = func(["of-tst"], conditional)
        return call(receive(toy.condition), f)
    if type(toy) == decl:
        toy.rhs = value(toy.rhs)
        return toy
    if type(toy) == declSequence:
        new_sequence = []
        for declaration in toy.sequence:
            new_sequence.append(split(declaration, k))
        toy.sequence = new_sequence
        toy.expr = split(toy.expr, k)
        return toy
    if type(toy) == grab:
        return declSequence([decl(toy.var, func(["x", "f"], call(k, "f"))), split(toy.rhs, k)])
    if type(toy) == list:
        if len(toy) < 1:
            return k  # ?
        else:
            call_arg = func(["of-rst"], call(k, "of-rst"))
            f = func(["of-fst"], call(receive(toy[1:]), call_arg))
            return call(receive(toy[0]), f)
    if type(toy) == stop:
        return stop(receive(toy.toy))

# ParsedToy -> ParsedToy
# Special casing for function and integers (The possible RHS of Decl)
# Want to get the value directly, not nesting in another function (Prevent inf loops)
def value(toy):
    global COUNT
    if type(toy) == int:
        return toy
    else:
        COUNT += 1
        return func([new_var("k", COUNT)] + toy.args, split(toy.body, new_var("k", COUNT)))

# ParsedToy, String -> ParsedToy
# Auxiliary function for handling calls
# Longer due to have to use the functionality of multi-arg calls as the
# last expression of a multi-arg function call
def split_call(toy, k):
    global COUNT, FCOUNT
    if not toy.params:  # Case for no argument function calls
        if type(toy.fun) == str:
            return call(toy.fun, k)
        elif type(toy.fun) == func:
            return call(value(toy.fun), k)
        else:
            return call(split(toy.fun, k), k)
    else:  # Normal case for any-argument calls
        received_expr = []
        function_args = []
        expressions = toy.params[::-1] + [toy.fun]
        for i in range(FCOUNT, len(expressions) + FCOUNT):
            function_args.append(new_var("f", i))
        FCOUNT += len(expressions)
        last_expr = call(function_args[-1], [k] + function_args[0:-1][::-1])
        for i in range(len(expressions)):
            received_expr.append(receive(expressions[i]))
        function_args.reverse()
        received_expr.reverse()
        for i in range(len(function_args)):
            last_expr = call(received_expr[i], func(function_args[i], last_expr))
    return last_expr
