from errors import UndeclaredException

# Environment is a [[(var, storeLocation)]]
class environment:
    def __init__(self):
        self.stack = []

    # (var storeLocation) -> None
    # adds the given var to the end of the last list
    def pushTo(self, var, index):
       self.stack.append((var, index))

    # var -> storeLocation | Undeclaired Exception
    # returns the storeLocation for the given var or errors
    def lookUp(self, var, store):
        mostRecent = self.stack[::-1]
        for pair in mostRecent:
            if pair[0] == var:
                return pair[1]
        raise UndeclaredException(var, store)

    # var -> boolean
    # returns true if the var is defined in the environment
    def is_in(self, var):
        return any(var == x for x in self.stack)

    def __str__(self):
        print("WORKING @ ", len(self.stack))
        var_list = self.stack
        for i, item in enumerate(var_list):
            print(i, "Var:", item[0], ", value:", item[1])
        return ""
    def __repr__(self):
        print("WORKING @ ", len(self.stack))
        var_list = self.stack
        for i, item in enumerate(var_list):
            print(i, "Var:", item[0], ", value:", item[1])
        return ""