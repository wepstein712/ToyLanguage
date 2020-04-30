#!/usr/bin/env python

from decl import decl
from func import func
from call import call
from cond import cond
from declSequence import declSequence

# ParsedVExpr is one of:
# - Str
# - Int
# - Node
# - [Decl*, ParsedVExpr]

# SD is one of:
# - ParsedVExpr
# - [Int, Int]

# Str, ParsedVExpr, Int, Int, Int -> SD (With only variable references changed to [Int, Int])
# Changes all of the references for a variable into an array of [Depth, Index] ([Int, Int])
def sd(var, data, depth, index, context):
    if type(data) == str:
        if data == var:
            return [depth, index]
        else:
            return "_"
    elif type(data) == int:
        return data
    elif type(data) == func:
        rightness = 0
        for arg in data.args:
            if arg != var:
                data.body = sd(var, data.body, depth + 1, index, context)
                data.body = sd(arg, data.body, 0, rightness, context + 1)
            else:
                data.body = sd(arg, data.body, depth, index, context + 1)
            rightness += 1
        removed_s = []
        for s in data.args:
            removed_s.append("_")
        data.args = removed_s
        return data
    elif type(data) == call:
        param_list = []
        for param in data.params:
            param_list.append(sd(var, param, depth, index, context))
        f = sd(var, data.fun, depth, index, context)
        return call(f, param_list)
    elif type(data) == cond:
        condition = sd(var, data.condition, depth, index, context)
        t = sd(var, data.true_expression, depth, index, context)
        f = sd(var, data.false_expression, depth, index, context)
        return cond(condition, t, f)
    elif type(data) == decl:
        if data.var != var:
            data.rhs = sd(var, data.rhs, depth, index, context)
            data.rhs = sd(data.var, data.rhs, 0, context, context)
        else:
            data.rhs = sd(data.var, data.rhs, 0, context, context)
        data.var = "_"
        return data
    elif type(data) == declSequence:
        seq = data.sequence
        seq.append(data.expr)
        new_sequence = sd(var, seq, depth, index, context)
        return declSequence(new_sequence)
    elif type(data) == list:
        if len(data) > 1:
            if type(data[0]) == decl:
                data[1:] = sd(data[0].var, data[1:], depth, context, context + 1)
            data[1:] = sd(var, data[1:], depth, index, context + 1)
            data[0] = sd(var, data[0], depth, index, context)
        else:
            if type(data[0]) == list:
                depth += 1
            data[0] = sd(var, data[0], depth, index, context)
        return data

