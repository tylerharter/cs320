# Linting in order to write good code

## Clarifications/Corrections

* none yet

## Introduction

According to [Wikipedia](https://en.wikipedia.org/wiki/Lint_(software)):
"Lint, or a linter, is a tool that analyzes source code to flag programming errors, bugs, stylistic errors, and suspicious constructs."

As such, linting software allows a programmer to write higher quality code by letting them know what might be wrong or erroneous with their code. 
For this reason, we highly encourage you to use this program.

## Installation

We've provided a file called `lint.py` that will lint any file you pass to it. First start by downloading it.
Then you'll need to install dependencies. This linting script relies on three libraries: nbformat, numpy and pylint. 
You should already have the first two installed from previous projects (note: nbformat comes with jupyter) 
so let's just install pylint like so:  
```
pip install pylint
```

Then download the `lint.py` file above and place it in the directory where the code you want to lint is. 
Next, navigate to that directory with `cd`.

Reminder: Based on your setup, you might need to prefix `python3 -m` or `py -m` or something else to run the command above.  

## How it works

Now that it is downloaded and dependencies installed, we are ready to run it.
Let's start be first seeing what arguments it is expecting. Since this program is 
meant to be ran from the command line we call it a command line interface (CLI) and 
a standard for CLIs is to accept the `-h` or `--help` to display information about the program.

Let's try it:

```
python3 lint.py -h
```

This will display the following:

```
usage: lint.py [-h] [-v] path

Linter for CS320

positional arguments:
    path           path of file to lint (.ipynb or .py)

optional arguments:
    -h, --help     show this help message and exit
    -v, --verbose  by default don't show warnings nor convention messages,
                   enable with -v and -vv respectively
```

Therefore we need to provide a path to the file we want to lint. Also, notice there's a 
verbosity flag. By passing `-v` or `-vv` we can get more and more specific messages. 
Without these we would only get messages that are refactor messages (i.e: advice on how to simplify code) 
and error messages. With `-v` we also get warnings. The most verbose (explicity) option is `-vv` 
and this will also give messages about python coding style conventions. 

Note that due to the way the linter processes jupyter notebooks some convention messages might be inaccurate. 
However, we would still encourage you to experiment with different linting verbosity levels.

There's up to four types of messages that this linter will provide:
1. Error messages: things like invalid syntax or weird characters
    * You are likely not to see these if your code works. 
2. Refactor messages: see below for an example of this
    * Won't catch everything, try to create functions where applicable don't rely on this.
3. Warnings: things like redefining built-in variable names (i.e: dict, len, list...) 
    * Only displayed with `-v`
4. Convention messages: Python has a standard set of rules regarding what code should look 
like (called [PEP8](https://www.python.org/dev/peps/pep-0008/)), these messages signify the 
code style is not on par with these style guides.
    * Only displayed with `-vv`. Some of these might be incorrect when linting notebooks.

## Examples

If we save the following snippet in a program called badcode.py

```python
for i in range(10):
    if i == 1 or i == 3 or i == 5 or i == 7 or i == 9:
            print('i is odd')
    else:
        print('i is even')
```

And then run 

```python
python3 lint.py badcode.py
```

We get the following output 

```
Refactor Messages:                                                                                                      
line: 2 - Consider merging these comparisons with "in" to 'i in (1, 3, 5, 7, 9)' 
```

This indicates there's an easy way to simplify our code. So lets try it! Change the code to this:

```python
for i in range(10):
    if i in (1, 3, 5, 7, 9):
            print('i is odd')
    else:
        print('i is even')
```

Much nicer right? Lets rerun the linter but with increased verbosity to see if it catches anything else. 
Rerunning it with the `-v` flag we get: 

```
Warning Messages:                                                                                                       
line: 3 - Bad indentation. Found 12 spaces, expected 8  
```

Indeed, our indent for the first print is not correct. Note that a tab is generally equal to 4 spaces, so 
it is saying you tabbed twice instead of once.

Obviously this example is rudimentary and only meant to illustrate how this works, but linting can really help.

## Linting jupyter notebooks 

Linting a notebook works the same way as linting a python script. The linter
will automatically detect that the file is a notebook, then convert it to a 
`.py` file with the same name, perform linting on this, and then try to convert the
line numbers from that file to a cell/line number.

You can enable line numbers in cells like so:

![img](https://i.stack.imgur.com/4VWQf.png)

The cell number is a little tricky. Say we get a message that starts with something 
like `cell: 2, line: 2`. This refers to the second cell _**that is non empty**_ 
of the notebook, at line 2. An easy way of finding the correct cell is to restart 
and run all and then the correct cell number will be the one in the brackets next 
to the cell, in this case `In[2]:`


## Common Pitfalls

It is important to realize that a linter cannot magically guess what the intent of your code is. Instead, 
it simply applies a ton of predefined rules (known as heuristics) to your source code to see if anything *seems* 
incorrect, involuntary or wrong. This means that a linter, even the best ones, cannot help you fix broken code. 
It can only help you make code more concise and readable. 

Because of this, linters might not give a warning message where one is due or they might instead produce extra 
messages, so please always take linting messages with a grain of salt.

Let's save the following code in badcode.py:

```python
found = False

for i in range(10):
    print(i)
    if i == 5:
        found = True
    break

print(found)
```

Running this we see that the output is:

```
0
False
```

What's going on? Is 5 not in the range(10)? We'll it is, but the problem is that we break right away.
Instead we should indent the break statement one more such that it's in the if block. This might 
be obvious to you but the linter has no idea what is meant to happen and thus instead of showing a 
message like before that said the indent was incorrect, it will simply print something like:

```
No linting messages to show!
```


