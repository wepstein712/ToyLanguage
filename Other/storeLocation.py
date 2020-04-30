class storeLocation:
    """
    The location of a given stored Parsed_SFVExpr in the Store
    Always a Natural Number
    """
    def __init__(self):
        self.loc = 0
        self.gen = 0

    def __init__(self, location, gen =0):
        self.loc = location
        self.gen = gen

    def __eq__(self, other):
        if isinstance(other, storeLocation):
            return self.loc == other.loc
        return False

    def __int__(self):
        return self.loc

    def __str__(self):
        # return "[\"cell\", " + str(self.loc) + "]"
        return "\"cell\""

    def __repr__(self):
        # return "[\"cell\", " + str(self.loc) + "]"
        return "\"cell\""
