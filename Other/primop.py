from errors import ArgumentParameterMismatch, PrimopDomainError

class primop:

    def __init__(self):
        self.name = ""
        self.primop = None
        self.arity = 0

    def __init__(self, name, function, arity):
        self.name = name
        self.primop = function
        self.arity = arity

    # Apply the primop function with the given arg list
    # [value]* -> value
    def apply(self, args):
        if len(args) == self.arity:
            try:
                return self.primop(args)
            except (TypeError, AttributeError):
                raise PrimopDomainError(args[-1])
        raise ArgumentParameterMismatch(args[-1])

    def __repr__(self):
        return self.name +  str(self.arity)
        return "\"primop\""

    def __str__(self):
        return self.name + " [" + str(self.arity) + "]"
        return "\"primop\""
