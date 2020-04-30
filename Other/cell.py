# box that holds an Int | Func
class cell:
    def __init__(self):
        self.content = 0

    def __init__(self, content):
        self.content = content

    # '
    # Gets the current content of the cell
    # -> value
    def get(self):
        return self.content

    # '
    # Sets the current content of the cell to the given value
    # value ->
    def set(self, val):
        self.content = val

    # '
    # Gets the current value of the cell, then sets the new value to the cell's value
    # value -> value
    def getset(self, new_val):
        val = self.get()
        self.set(new_val)
        return val

    def __repr__(self):
        # if type(self.contents) == cell:
        #     return "[cell " + str(self.contents) + "]"
        # if type(self.contents) == func:
        #     return '\"closure\"'

        return str(self.content)

    def __str__(self):
        # if type(self.contents) == cell:
        #     return "[cell " + str(self.contents) + "]"
        # if type(self.contents) == func:
        #     return '\"closure\"'
        return str(self.content)
