# Lab 4: Linked Lists

Most people learn about Python lists before they learn about Python
classes.  But what if you learned about classes first, and Python
didn't already have a list data type -- could you build your own list
using classes?

There are many different ways to create data structures that work like
lists.  One simple but recursive design is the *linked list*.  Linked
lists are represented by *Node* objects:

A *Node* object has a value and potentially refers to another Node object

A Node object that does not refer to another Node represents a list
with one value.  A two-value list consists of two nodes: the first
refers to the second, and the second doesn't refer to anything.

## Basic Example

Start by pasting the following:

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

L = Node(3)
L2 = Node(5)
L3 = Node(7)
L.next = L2
L2.next = L3
```

It's a good idea to visualize the [above code](http://pythontutor.com/live.html#code=class%20Node%3A%0A%20%20%20%20def%20__init__%28self,%20val%29%3A%0A%20%20%20%20%20%20%20%20self.val%20%3D%20val%0A%20%20%20%20%20%20%20%20self.next%20%3D%20None%0A%0AL%20%3D%20Node%283%29%0AL2%20%3D%20Node%285%29%0AL3%20%3D%20Node%287%29%0AL.next%20%3D%20L2%0AL2.next%20%3D%20L3&cumulative=false&curInstr=18&heapPrimitives=nevernest&mode=display&origin=opt-live.js&py=3&rawInputLstJSON=%5B%5D&textReferences=false) step-by-step in PythonTutor.

Paste the code in a notebook.  To get the value at index 0, run the following:

```python
L.val
```

To get the value at index 1, run the following:

```python
L.next.val
```

Write a snippet to get the value at index 2:

```python
L.next.????
```

## Length

If you try `len(L)`, `len(L2)`, etc., it won't work, because the Node
class doesn't have a `__len__` method next.  Try adding it inside your `Node` class:

```python
    def __len__(self):
        if self.next == None:
            # base case: I'm the only Node!  Length must be 1
            return 1
        else:
            # recursive case: total length is the length of next plus 1
            raise NotImplemented("recursive case not implemented yet")
```

Test it with `len(L3)`.  It should work.  What about `len(L)` and
`len(L2)`?  Get rid of the `NotImplemented` exception and right a
return statement for the recursive case, then test those again.  If
you're really stuck, check the [hints](hint.md#length).

## Representation

It would be nice to add a function that lets us represent our list as
a string.  Paste and finish:

```python
    def __????__(self):
        if self.next == None:
            return repr(self.val)
        else:
            return repr(self.val)+","+repr(self.next)
```

[Hints if Really Necessary](hint.md#representation)

## Indexing

To make indexing work, we need to implement `__getitem__`.  The zero
index is the easiest case: `L[0]` should produce the same value as
`L.val`.  This is the base case.  Paste and finish:

```python
    def __getitem__(self, idx):
        if ???? == 0:
            # base case
            return ????
        else:
            # recursive case
            return self.next[idx-1]
```

[Hints if Really Necessary](hint.md#indexing)

## Looping

Try this:

```python
for x in L:
    print(x)
```

You'll get an error because the `for` loop just keeps trying bigger
indexes until it falls off the end (it does not check the length
first).  To make the above work cleaner, add this check before the
recursive case in your `__getitem__` method:

```python
            if self.next == None:
                raise IndexError()

            # recursive case
```

Try running the for loop again -- work better now?

## Negative Indexing

Can you get negative indexing (e.g., `L[-1]`) working?  Here's a clue:

```python
regular_list = ["A", "B", "C", "D"]
neg_idx = -2
pos_idx = 4 + neg_idx # where did 4 come from?
print(regular_list[neg_idx])
print(regular_list[pos_idx])
```

[Hints if Really Necessary](hint.md#negative-indexing)

## Append

We just need a regular method for this one (not a `__methodname__`
special method).

To append, we need to navigate through the chain of `next`'s until we
reach the end, then add a new node there.

It's possible to do this with either recursion or a loop -- you pick!
Here's some started code if you want to do it with the loop:

```python
    def append(self, val):
        last_node = self
        while last_node.???? != ????:
            last_node = last_node.????
        last_node.next = ????
```

Give it a test:

```python
L = Node("A")
L.append("B")
L.append("C")
print(L)
```

## ABCs

Try importing the `abc` module in Python (read about it [here](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)):

```python
from collections import abc
```

"ABC" stands for "Abstract Base Class", which means a class that's not
meant to directly create objects -- it's only purpose is to be a
parent for other classes.  This is an easy way to get extra features.

For example, if our class implements `__getitem__` and `__len__`
(which it already does), and we inherit from `abc.Sequence`, we'll get
`.index(...)` and `.count(...)` methods for free.

Change `Node`'s class declaration to inherit from Sequence:

```python
class Node(abc.Sequence):
```

```python
L = Node("A")
L.append("B")
L.append("B")
L.append("C")
L.append("D")
print("List:", L)
print("A is at index", L.index("A"))
print("C is at index", L.index("C"))
print("B occurs", L.count("B"), "times")
print("D occurs", L.count("D"), "times")
```

You should see something like this:

```
List: 'A','B','B','C','D'
A is at index 0
C is at index 3
B occurs 2 times
D occurs 1 times
```

We get two useful methods, `.index(...)` and `.count(...)` by only
adding one parent class.  Pretty cool, huh?

## Concluding Thoughts

Although we were able to implement something that works somewhat like
a Python list, it wouldn't be a good idea to use our version as is.
With a regular Python list, index lookups to the last items (like
`L[-1]`) are fast -- they have O(1) complexity.  Although
`__getitem__` doesn't use a loop, the recursion still need to go
through every node to find the last one, so `L[-1]` is an `O(N)`
operation for our version of the list -- ouch.
