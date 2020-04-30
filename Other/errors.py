"""
    Here are our exceptions that can be thrown in expected cases where the program should error.
    The last error was something that we included while doing testing for pointer location manipulation, but is not
    necessary for the program.
"""

class UndeclaredException(Exception):
    def __init__(self, var, store):
        self.var = var
        self.store = store

    def __str__(self):
        return "\"variable " + str(self.var) + " undeclared\""


class ArgumentParameterMismatch(Exception):
    def __init__(self, store):
        self.store = store

    def __str__(self):
        return "\"number of arguments does not match number of parameters\""


class ClosureOrPrimopExpected(Exception):
    def __init__(self, store):
        self.store = store

    def __str__(self):
        return "\"closure or primop expected\""


class PrimopDomainError(Exception):
    def __init__(self, store):
        self.store = store

    def __str__(self):
        return "\"primop domain error\""


class SegfaultError(Exception):
    def __init__(self, store):
        self.store = store

    def __str__(self):
        return "\"invalid store access error\""

class exponentiationError(Exception):
    # Error for the case of [Integer, "^", (Integer < 0)]
    def __str__(self):
        return "primop domain error"

class StopContinuation(Exception):
    def __init__(self, toy, env, store):
        self.toy = toy
        self.env = env
        self.store = store