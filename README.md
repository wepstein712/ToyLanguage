# Toy Programming Language

The Toy programming language is a limited JSON based language to emulate basic functionality and to explore 
the core of modern computer languages and their roots. Implemented in Python, it allows for the creation and 
use of functions, variables, and conditionals. 


This version of the programming langauge uses continuation passing style to allow for program flow control. 
## Definition
A *Toy* is one of:
* a Var
* an Int
* a JSON array of the shape [Tdecl,...Tdecl, Toy], where all variables declared in one Tdecl are pairwise distinct. This 
will declare all vars defined in the Tdecls of the array, and then interpret and return the value of the Toy in the end of the array.
* a JSON array of the shape ["fun*", [var,...,var], Toy], where all variables in one Varlist are pairwise distinct. 
This defines a function that takes in at least 0 arguments, and then returns the value given by interpretting the Toy. 
* a JSON array of the shape ["call, Toy, Toy,...,Toy]. This will invoke the first Toy as if it were a function, and pass 
the remainder of the Toy expressions as arguments to the function.
* a JSON array of the shape ["if-0, Toy, Toy, Toy]. This conditional statement will evaluate the first Toy expression, 
if it equals zero, then it will evaluate only the second Toy expression, otherwise it will only evaluate the third.
* a JSON array of the shape ["seq*, Toy, Toy,...,Toy]. This statement evaluates the non-empty sequence of Toy 
expressions in order and returns the result of the last expression as its own.
* a JSON array of the shape ["grab", Var, Toy]. This statement turns the continuation of the grab expression into a 
closure, binds it to the specified Var, and evaluates the “body” expression to obtain a value.
* a JSON array of the shape ["stop", Toy]. This statement eliminates its continuation and 
then evaluates its sub-expression to obtain the final answer.

A Tdecl is:
* a JSON array of the shape ["let", Var, "=", Int]
* a JSON array of the shape ["let", Var, "=", ["fun*",  [var,...,var], Toy]]

Prelude:
The prelude is the given set of primitive operators that are given for "free" by the language. The prelude for this includes:
* + -> The plus operation will add 2 integers.
* * -> The multiplication operation will multiply 2 integers.
* ^ -> The exponentiation operation will raise the first integer to the power of the second.
* @ -> The At operation will take a value and place it in the store and return a cell with the cell location of that value in it.
* ! -> The Bang operation consumes a single value, a cell, and retrieves the current value in the location specified by that cell.
* = -> The Equal operation consumed two arguments, a cell and an arbitrary value, sticks this value into the cell, 
    and returns the value that was in the cell already.

## How to run
The program can be run by using the *xrun* excecutable in this directory. In your terminal you may input one of two options:
```bash
./xrun < INPUT
```
where input is the path to a JSON file that follows the syntax laid out above. Additionly you may input the code directly 
to the program with:
```bash
./xrun
```
And then typing out the program by hand. Once you complete your program, add an end-of-file character to signal the end 
input.

Tests can be found in the ITests folder

