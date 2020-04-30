"""
Internal representation of a ["call", Toy, Toy, ..., Toy]
A call has a:
    - fun = func object
    - params = [ParsedToy]*
"""
class call:
    def __init__(self):
        self.fun = None
        self.params = None

    def __init__(self, fun, params):
        self.fun = fun
        self.params = params
        if type(params) != list:
            self.params = [params]

    def __eq__(self, other):
        if isinstance(other, call):
            return self.fun == other.fun and self.params == other.params
        return False

    def __repr__(self):
        p_string = ""
        for p in self.params:
            if type(p) == str:
                p_string += "\"" + str(p) + "\"" + ", "
            else:
                p_string += str(p) + ", "
        if len(self.params) > 0:
            p_string = p_string[:-2]
        if type(self.fun) == str:
            return "[\"call\", \"" + str(self.fun) + "\", " + p_string + "]"
        return "[\"call\", " + str(self.fun) + ", " + p_string + "]"

    def __str__(self):
        p_string = ", "
        for p in self.params:
            if type(p) == str:
                p_string += "\"" + str(p) + "\"" + ", "
            else:
                p_string += str(p) + ", "
        p_string = p_string[:-2]
        if type(self.fun) == str:
            return "[\"call\", \"" + str(self.fun) + "\"" + p_string + "]"
        return "[\"call\", " + str(self.fun) + "" + p_string + "]"
