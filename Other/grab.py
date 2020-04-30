# internal representation of ["grab", var, Toy]
class grab:
    def __init__(self):
        self.var = None
        self.rhs = None

    def __init__(self, var, toy):
        self.var = var
        self.rhs = toy

    def __repr__(self):
        return "[\"grab\", \"" + self.var + "\", " + str(self.rhs) + "]"

    def __str__(self):
        return "[\"grab\", \"" + self.var + "\", " + str(self.rhs) + "]"