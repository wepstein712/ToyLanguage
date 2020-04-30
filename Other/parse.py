#!/usr/bin/env python

import sys
import json
from decl import decl
from func import func
from call import call
from cond import cond
from declSequence import declSequence
from grab import grab
from stop import stop
import random
import string
'''
A ParsedToy is one of:
    - Var (String)
    - Integer
    - Decl
    - DeclSequence
    - Func
    - Call
    - Cond
    - Grab
    - Seq
    - Stop
A JSON is the Toy formatted JSON input
'''

# int -> [string*]
# Creates an n-length list of random strings
def rand_stringer(num):
    res_list = []
    for i in range(num):
        res_list.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=5)))
    return res_list

# JSON -> ParsedToy
# Turns the json input into the internal representation
def parseList(jso):
    if len(jso) > 0:
        if jso[0] == "fun*":
            body = parse(jso[2])
            return func(jso[1], body)
        if jso[0] == "call":
            params = []
            for parameter in jso[2:]:
                params.append(parse(parameter))
            c = call(parse(jso[1]), params)
            return c
        if jso[0] == "if-0":
            return cond(parse(jso[1]), parse(jso[2]), parse(jso[3]))
        if jso[0] == "let":
            return decl(jso[1], parse(jso[3]))
        # No need for infix operation checking in the list section, since it cannot happen
        if jso[0] == "seq*":
            args = []
            for s in jso[1:-1]:
                p = parse(s)
                args.append(p)
            f = call(func(rand_stringer(len(args)), parse(jso[-1])), args[::-1])
            return f
        if jso[0] == "grab":
            return grab(parse(jso[1]), parse(jso[2]))
        if jso[0] == "stop":
            return stop(parse(jso[1]))
        if type(jso) == list:
            return_array = []
            for item in jso:
                return_array.append(parse(item))
            if len(return_array) > 1 and type(return_array[0]) == decl:
                return declSequence(return_array)
            return return_array
    return jso


# JSON -> ParsedToy
# Turns the json input into the internal representation
def parse(jso):
    if type(jso) == str:
        return jso
    elif type(jso) == int:
        return jso
    elif type(jso) == list:
        return parseList(jso)


def main():
    line = sys.stdin.read()
    jso = json.loads(line.encode('ascii', 'ignore'))
    print("JSON:", jso)
    print("-------------------------------------")
    print("Our Object:", parse(jso))
    print("Type:", type(jso))


if __name__ == "__main__":
    main()
