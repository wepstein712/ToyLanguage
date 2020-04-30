from sd import sd
from copy import deepcopy

# ParsedToy, ParsedToy -> Boolean
# Returns True if the toy expressions match (Ignoring variable names), False otherwise
# Relies heavily on the equality methods of the ParsedToy classes
def alpha_equal(a, b):
    st_a = sd("", deepcopy(a), 0, 0, 0)
    st_b = sd("", deepcopy(b), 0, 0, 0)
    return st_a == st_b
