"""
Internal representation of a ["let", Var, "="", Toy]
where the Toy has to represent an Integer or ["fun*"...]
A cond has a:
    - var = String
    - rhs = ParsedToy
"""
class decl:
    def __init__(self):
        self.var = None
        self.rhs = None

    def __init__(self, varName, rhs):
        self.var = varName
        self.rhs = rhs

    def __eq__(self, other):
        if isinstance(other, decl):
            return self.var == other.var and self.rhs == other.rhs
        return False

    def __repr__(self):
        return "[\"let\", \"" + self.var + "\", \"=\", " + str(self.rhs) + "]"

    def __str__(self):
        return "[\"let\", \"" + self.var + "\", \"=\", " + str(self.rhs) + "]"
