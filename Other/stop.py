class stop:
    def __init__(self):
        self.toy = None

    def __init__(self, toy):
        self.toy = toy

    def __repr__(self):
        if type(self.toy) == str:
            toy_string = "\"" + self.toy + "\""
        else:
            toy_string = str(self.toy)
        return "[\"stop\"," + toy_string + "]"

    def __str__(self):
        if type(self.toy) == str:
            toy_string = "\"" + self.toy + "\""
        else:
            toy_string = str(self.toy)
        return "[\"stop\"," + toy_string + "]"
