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
