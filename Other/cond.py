"""
    A cond is the internal representation of a ["if-0", Toy, Toy, Toy] statement
    cond is:
    - condition = ParsedToy
    - true_expression = ParsedToy
    - false_expression = ParsedToy
"""
class cond:
    def __init__(self, condition, t, f):
        self.condition = condition
        self.true_expression = t
        self.false_expression = f

    def __eq__(self, other):
        if isinstance(other, cond):
            return self.condition == other.condition and self.true_expression == other.true_expression and\
                   self.false_expression == other.false_expression
        return False

    def __str__(self):
        cond_quotes = ""
        if type(self.condition) == str:
            cond_quotes = "\""
        t_quotes = ""
        if type(self.true_expression) == str:
            t_quotes = "\""
        f_quotes = ""
        if type(self.false_expression) == str:
            f_quotes = "\""
        return "[\"if-0\", " + cond_quotes + str(self.condition) + cond_quotes +\
               ", " + t_quotes + str(self.true_expression) + t_quotes + ", " +\
               f_quotes + str(self.false_expression) + f_quotes + "]"

    def __repr__(self):
        cond_quotes = ""
        if type(self.condition) == str:
            cond_quotes = "\""
        t_quotes = ""
        if type(self.true_expression) == str:
            t_quotes = "\""
        f_quotes = ""
        if type(self.false_expression) == str:
            f_quotes = "\""
        return "[\"if-0\", " + cond_quotes +  str(self.condition) + cond_quotes +\
               ", " + t_quotes + str(self.true_expression) + t_quotes + ", " +\
               f_quotes + str(self.false_expression) + f_quotes + "]"
