"""
Internal representation of an ordered list of decls that need to be allocated,
and then stored in the env, store from l->R
A declSequence has a:
    - sequence = [decl]*
        - the sequence of decl expressions that need to be interpreted
    - expr = ParsedToy
        - is the last item in the decl list
"""
class declSequence:
    def __init__(self):
        self.sequence = []
        self.expr = None

    def __init__(self, sequence):
        self.sequence = sequence[:-1]
        self.expr = sequence[-1]

    def __eq__(self, other):
        if isinstance(other, declSequence):
            return self.sequence == other.sequence and self.expr == other.expr
        return False

    def __repr__(self):
        decl_string = ""
        if type(self.sequence) == list:
            for dec in self.sequence:
                decl_string += str(dec) + ", "
            decl_string = decl_string[:-2]
        else:
            decl_string = str(self.sequence)
        return "[" + decl_string + ", " + str(self.expr) + "]"

    def __str__(self):
        decl_string = ""
        if type(self.sequence) == list:
            for dec in self.sequence:
                decl_string += str(dec) + ", "
            decl_string = decl_string[:-2]
        else:
            decl_string = str(self.sequence)
        return "[" + decl_string + ", " + str(self.expr) + "]"
