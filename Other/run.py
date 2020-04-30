import random
import string
import json
import sys

from call import call
from stop import stop
from cps import receive
from func import func
from parse import parse
from interpreter import interp_ast
from prelude import opList

RESERVED_STRINGS = ["fun*", "grab", "call", "if-0", "let", "=", "stop", "seq"]

# JSON Object, [String] -> [String]
# Takes in a JSON object and collects all non-keyword/prim-op strings
def collect_strings(jso, collected):
    if type(jso) == str and (jso[0] == "k" or jso[0] == "f"):
        if jso not in collected and jso not in RESERVED_STRINGS and jso not in opList:
            collected.append(jso)
        return collected
    elif type(jso) == list:
        for item in jso:
            collected = collect_strings(item, collected)
        return collected
    return collected

# JSON Object, {String:String} -> JSON Objects
# Takes in a JSON object and mapping of original -> new variable names
# Uses the mapping to replace all occurrences of the original to the new
def replace_strings(jso, mapping):
    if type(jso) == str:
        if jso in mapping.keys():
            jso = mapping[jso]
        return jso
    elif type(jso) == list:
        new_jso = []
        for item in jso:
            new_jso.append(replace_strings(item, mapping))
        return new_jso
    return jso

# JSON Object, [String] -> [String]
# Creates the mapping of the old -> new strings and then replaces the new ones
def change_strings(jso, collected):
    string_mapping = {}
    for s in collected:
        new_string = s
        while new_string in collected:
            new_string = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        string_mapping[s] = new_string
    return replace_strings(jso, string_mapping)

# converts toy into its cps form, puts a wrapper around it, and interprets the result
# ParsedToy -> Value
def run(toy):
    app_form = func(["x"], stop("x"))
    cps_form = call(receive(toy), app_form)
    interp_ast(cps_form)

def main():
    line = sys.stdin.read()
    jso = json.loads(line.encode('ascii', 'ignore'))

    # Call the name protection/randomization functions,
    # replaces any user-input functions that could match our
    # generated function/variable names
    strings = collect_strings(jso, [])
    jso = change_strings(jso, strings)
    toy = parse(jso)
    run(toy)

if __name__ == '__main__':
    main()