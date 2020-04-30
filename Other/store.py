from cell import cell
from prelude import ops
from errors import SegfaultError
from storeLocation import storeLocation


class store:
    """
        Representation of space in memory
        Store is:
        - [cell*]
    """

    def __init__(self):
        self.cellBlock = []

    # Parsed_SFVExpr -> StoreLocation (the location in the cellblock where this resides)
    # this gets called when creating a NEW location in memory
    def alloc(self, entry =0):
        newCell = cell(entry)
        self.cellBlock.append(newCell)
        return storeLocation(len(self.cellBlock) - 1)

    # Parsed_SFVExpr -> StoreLocation (the location in the cellblock where this resides)
    # this gets called when creating a NEW location in memory
    def alloc_generated(self, entry=0):
        newCell = cell(entry)
        self.cellBlock.append(newCell)
        return storeLocation(len(self.cellBlock) - 1, 1)

    # gets what is in the cell at the given index
    # natural number -> Parsed_SFVExpr
    def getAt(self, index):
        if type(index) == storeLocation:
            index = index.loc
        if index < 0 or index >= len(self.cellBlock):
            # exclusively used for testing
            raise SegfaultError()
        return self.cellBlock[index].get()

    # sets the contents of the cell at given index to the given value, then returns the value that was in the cell
    # natural number, Parsed_SFVExpr -> Parsed_SFVExpr
    def setAt(self, index, contents):
        if type(index) == storeLocation:
            index = index.loc
        if index < 0 or index >= len(self.cellBlock):
            # exclusively used for testing
            raise SegfaultError
        old_content = self.getAt(index)
        self.cellBlock[index].set(contents)
        return old_content

    def __repr__(self):
        ret_val = "[\"store\", ["
        for c in self.cellBlock[6:]:
            if type(c.get()) == str and c.get() in ops.keys():
                ret_val += '\"primop, \"'
            else:
                ret_val += str(c) + ", "
        ret_val = ret_val[0:-2]
        ret_val += "]]"
        return ret_val

    def __str__(self):
        ret_val = "[\"store\", ["
        for c in self.cellBlock[6:]:
            if type(c.get()) == str and c.get() in ops.keys():
                ret_val += '\"primop, \"'
            else:
                ret_val += str(c) + ", "
        ret_val = ret_val[0:-2]
        ret_val += "]]"
        return ret_val
