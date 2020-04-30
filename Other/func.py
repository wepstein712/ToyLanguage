"""
Internal representation of a ["fun*", [Var], Toy]
A func has a:
    - args = [String]*
    - body = ParsedToy
"""
class func:
    def __init__(self):
        self.args = None
        self.body = None

    def __init__(self, args, body):
        self.args = args
        self.body = body
        if type(args) != list:
            self.args = [args]

    def __eq__(self, other):
        if isinstance(other,  func):
            return self.args == other.args and self.body == other.body
        return False

    def __repr__(self):
        p_string = ""
        for p in self.args:
            if type(p) == str:
                p_string += "\"" + str(p) + "\"" + ", "
            else:
                p_string += str(p) + ", "
        if len(self.args) > 0:
            p_string = p_string[:-2]
        if type(self.body) == str:
            return "[\"func\", [" + p_string + "], " + "\"" + str(self.body) + "\"" + "]"
        else:
            return "[\"func\", [" + p_string + "], " + str(self.body) + "]"

    def __str__(self):
        p_string = ""
        for p in self.args:
            if type(p) == str:
                p_string += "\"" + str(p) + "\"" + ", "
            else:
                p_string += str(p) + ", "
        if len(self.args) > 0:
            p_string = p_string[:-2]
        if type(self.body) == str:
            return "[\"fun*\", [" + p_string + "], " + "\"" + str(self.body) + "\"" + "]"
        else:
            return "[\"fun*\", [" + p_string + "], " + str(self.body) + "]"
