from environment import environment
from store import store
from func import func
from call import call
from decl import decl
from cond import cond
from declSequence import declSequence
from funcValue import funcVal
from primop import primop
from prelude import ops
from storeLocation import storeLocation
from stop import stop
import copy
import errors
from parse import parse
import sys
import json

# handleList helps with exactly  the following cases:
# [ParsedToy*] environment store ->* value, store
def handleList(toy, env, store):
    """
    where handle list comes in:
     - single item lists
     - list of toy where the 2nd element will evaluate to a primop
    """
    if len(toy) == 1:
        return interpret(toy[0], env, store)
    else:
        # plan: interpret each item in list  R->L, check, then applyPrimop on [first, third->]
        prim, newStore = interpret(toy[1], env, store)
        if type(prim) == primop:
            args = toy[2:]
            args.insert(0, toy[0])
            return primopApply(prim, args, env, newStore)
        elif type(prim) == funcVal:
            args = toy[2:]
            args.insert(0, toy[0])
            return handleCall(call(toy[1], args), env, store)
        else:
            for i in toy[2:][::-1]:
                v, newStore = interpret(i, env, newStore)
            raise errors.ClosureOrPrimopExpected(newStore)


# takes the function and returns a closure (funcVal)
#   with the given store as part of itself
# ParsedToy env store ->* value store
def handleFunc(toy, env, store):
    fVal = funcVal(toy.args, toy.body, env)
    return (fVal, store)


# interprets lhs , lhs of toy on the store, then applies the function to them
# ParsedToy env store ->* value store
def handleCall(toy, env, store):
    """
    3 cases for toy:
      - func
      - str (referenceing a funcVal)
      - list that equates to a funkVal
    """
    fVal, store1 = interpret(toy.fun, env, store)
    if type(fVal) != funcVal and type(fVal) != primop:
        raise errors.ClosureOrPrimopExpected(store1)
    if type(fVal) == primop:
        return primopApply(fVal, toy.params, env, store1)
    if len(fVal.args) != len(toy.params):
        raise errors.ArgumentParameterMismatch(store1)

    argList = []
    newStore = copy.copy(store1)
    for arg in toy.params[::-1]:
        if type(arg) == str:
            argList.append((arg, env.lookUp(arg, newStore)))
        else:
            val, newStore = interpret(arg, env, newStore)
            argList.append((arg, val))

    return funApply(fVal, argList[::-1], newStore)


# Apply the primitive operation on the given arguments after interpreting
# primop [ParsedToy]* env store ->* value store
def primopApply(promise, argList, env, store):
    if promise.arity != len(argList) + 1:
        raise errors.ArgumentParameterMismatch(store)
    interpreted_args = []
    workingStore = copy.copy(store)
    for arg in argList[::-1]:
        val, workingStore = interpret(arg, env, workingStore)
        interpreted_args.append(val)
    interpreted_args.reverse()
    interpreted_args.append(workingStore)

    return promise.apply(interpreted_args)


# funValue [value]* ->* value, store
def funApply(functionValue, args, store):
    # allocated_params = []
    workingEnv = functionValue.workingEnv
    workingStore = copy.copy(store)

    for i, arg in enumerate(args):
        if type(arg[1]) == storeLocation:
            workingEnv.pushTo(functionValue.args[i], arg[1])
        else:
            sLoc = workingStore.alloc()
            workingStore.setAt(sLoc, arg[1])
            workingEnv.pushTo(functionValue.args[i], sLoc)

    return interpret(functionValue.body, workingEnv, workingStore)


# handle cond interprets the if-0 expression
# ParsedToy env store ->* value store
def handleCond(toy, env, store):
    condVal, store1 = interpret(toy.condition, env, store)
    if condVal == 0:
        return interpret(toy.true_expression, env, store1)
    return interpret(toy.false_expression, env, store1)


# interprets a sequence of decls & the toy at the end of it
# DeclSequence Env Store ->* value store
def handleDeclSeq(toy, env, store):
    # step 1: allocates all the space in the store for the # of decl's a
    # and point env for each decl to its place in the store
    listOfAllocatedStore = []
    workingStore = copy.copy(store)
    workingEnv = copy.copy(env)
    for dec in toy.sequence:
        loc = workingStore.alloc()
        listOfAllocatedStore.append(loc)
        workingEnv.pushTo(dec.var, loc)

    # step 2: interprets the rhs of each from L->R and assigns that value to the cell in the store
    for i, dec in enumerate(toy.sequence):
        val, workingStore = interpret(dec.rhs, workingEnv, workingStore)
        workingStore.setAt(listOfAllocatedStore[i], val)

    # step 3: interpret the toy.expr
    return interpret(toy.expr, workingEnv, workingStore)


# ParsedToy environment store ->* Value Store
# eliminates the continuation in the toy and then evaluates for a final answer
def handleStop(toy, env, store):
    if type(toy.toy) == str:
        raise errors.StopContinuation(toy.toy, env, store)
    raise errors.StopContinuation(call(toy.toy, func("asdasd", "asdasd")), env, store)

# ParsedToy environment store ->* Value Store
# determintes the value of toy
def interpret(toy, env, store):
    if type(toy) == str:
        # return lookup of the str and the store
        lookup = env.lookUp(toy, store)
        if type(lookup) == storeLocation and lookup.gen == 1:
          return lookup, store
        val = store.getAt(lookup)
        return val, store
    elif type(toy) == int:
        return toy, store
    elif type(toy) == func:
        # return a funcValue using the current env and the store
        return handleFunc(toy, env, store)
    elif type(toy) == call:
        # wrap the interpret (rhs, env, store) in a lambda
        # interpret lhs, env, store
        # apply fun on lhs rhs
        return handleCall(toy, env, store)
    elif type(toy) == cond:
        # evaluate condition == 0, then do the then or other
        return handleCond(toy, env, store)
    elif type(toy) == declSequence:
        return handleDeclSeq(toy, env, store)
    elif type(toy) == list:
        return handleList(toy, env, store)
    elif type(toy) == stop:
        handleStop(toy, env, store)


# wrapper for interpreter, does a try/except on interpreting and if its the stop continuation error
#   will just try it again
# ParsedToy environment store ->* Value Store
def stop_catch_interpretter(toy, env, store):
    try:
        return interpret(toy, env, store)
    except errors.StopContinuation as e:
        return stop_catch_interpretter(e.toy, e.env, e.store)


# performs setup for calling the interpreter
# ParsedToy -> None (prints the answer)
def interp_ast(toy):
    env = environment()
    s_store = store()
    for op in ops:
        env.pushTo(op[0], s_store.alloc())
        s_store.setAt(env.lookUp(op[0], s_store), op[1])
    try:
        answer, aStore = stop_catch_interpretter(toy, env, s_store)
        print(str(answer))

    # Catch all valid cases of exceptions thrown by the program itself
    except (errors.UndeclaredException, errors.PrimopDomainError, errors.ArgumentParameterMismatch,
            errors.ClosureOrPrimopExpected, errors.StopContinuation) as e:
            print(str(e))


# Main function of the program, what is ran when interpreter.py is called.
def main():
    line = sys.stdin.read()
    jso = json.loads(line.encode('ascii', 'ignore'))
    parsed_fvexpr = parse(jso)
    interp_ast(parsed_fvexpr)

if __name__ == "__main__":
    main()

