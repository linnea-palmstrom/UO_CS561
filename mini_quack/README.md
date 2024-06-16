# Example: Lark grammar to AST and symbol table

Here is a small example of parsing some
parts of the Quack language (class and 
method declarations), transforming 
the Lark parse tree into an AST with our
own custom classes, and then walking
the AST to populate a symbol table with 
class and method declarations. 

Thanks to Pranav Mathur for the initial
symbol table of built-in classes 
(in `qklib/builtin_methods.json`).
I have followed that structure in filling
in additional classes and methods from
the source file. 

## To Run

You must install lark before running. 
You can install it in a virtual 
environment as follows:
```shell
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
```

The second command above (with `activate`)
makes the virtual environment active. 

To run: 
```shell
python3 quack_front.py samples/blahblahblah.qk
```
The output should be a poorly indented
version of blahblahblah.qk with some 
"normalization", e.g., the constructor
methods are included as if they had been
enclosed in a method declaration.  Following
that you should find a symbol table
consisting of the contents of 
`builtin_methods.json` and a similar
record for the method `Point` from 
blahblahblah.  

To leave the virtual environment after
running the sample, you can use this 
command: 

```shell
deactivate
```

To compile and run the quack program on the tiny vm:
```shell
bash quack.sh samples/blahblahblah.qk
```

In order to run the bash script quack.sh, you
may have to modify the TVMDIR file path to
match the path to the tiny vm folder on your
personal computer. This script creates a
qkmain.asm assembly code file in the QkASM
folder of the tiny vm, creates a $Main.json
file inside of the OBJ folder of the tiny vm
and then runs the json file on the tiny vm.

## Problems with the compiler

Unfortunately, I have been having issues with
creating proper assembly code in the generated
qkmain.asm file, which I think is what is 
preventing the bash script from being able to 
generate the $Main.json file (the file that is 
created is empty and I get an error that says
"KeyError: 'program'" when I run the script with
the blahblahblah.qk file). I was looking at the 
parse tree, grammar and the quack transformer to 
see if I could figure out why the assembly code 
was not being generated properly. I noticed from 
the parse tree visualization produced by pydot 
when running the compiler with the blahblahblah.qk 
file that the parse tree, though matching closely 
to the grammar I had made, did not seem to match 
it exactly. For some reason, the parse tree does 
not include some of the nodes I created in the 
grammar. One example is when the value node points 
directly to the ident node when in my grammar it 
specifies that the value node should point to the 
name, int const or str const nodes instead. If I had
more time, I would have compared the parse tree
and the AST created from it to see where the issues
in creating these trees are. Since I was struggling
to generate the assembly code from the AST, I was
not able to implement the type inference part of the
quack compiler. Hopefully I will be able to implement
it during the summer.
