# Part 3: Efficient Queues

Appending to lists is generally O(1) and popping from the beginning is
O(N).  Do an experiment to show this is slow:

```python
from time import time

vals = list(range(200000)) # 200K
total = 0

t0 = time()
while len(vals) > 0:
    total += vals.pop(0)
t1 = time()
print("SUM:", total)
print("SECONDS:", t1-t0)
```

For certain types of graph search, we'll need a data structure where
we can efficiently append to the end and pop from the front.  Such a
data structure is called a queue.  Among other things, it's important
to know about queues for certaing artificial algorithms.

`deque` is the name of the a queue data structure that comes with
Python.  Read a bit about it:
https://docs.python.org/3/library/collections.html#deque-objects.
Note that a lot of documentation assumes readers understand big-O
notation.

Try running this experiment now:

```python
from time import time
from collections import deque

vals = deque(range(200000)) # 200K
total = 0

t0 = time()
while len(vals) > 0:
    total += vals.popleft()
t1 = time()
print("SUM:", total)
print("SECONDS:", t1-t0)
```

A little faster, huh?

Note that `deque` doesn't have a general purpose `pop` method, but it
has two methods for efficiently popping from the front and end of the
queue.

A structure used to add and remove values just from the end is called
a stack.  We won't learn a new data structure for the stack use case
because regular Python lists make for pretty efficient stacks.