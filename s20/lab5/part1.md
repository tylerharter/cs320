# Part 1: BSTs (Binary Search Trees)

In this lab, you'll create a BST that can be used as a dictionary.

## Basics Node and BST classes

Start by pasting+completing the following:

```python
class Node():
    def __init__(self, key, val):
        self.key = ????
        self.val = val
        self.left = None
        ????
```

Let's create a `BST` class with an `add` method that automatically
places a node in a place that preserves the search property (i.e., all
keys in left subtree are less than a parent's value, which is less
than those in the right tree).

Add+complete with the following.  Note that this is a non-recursive version of `add`:

```python
class BST():
    def __init__(self):
        self.root = None
        self.size = 0

    def add(self, key, val):
        if self.root == None:
            self.root = ????

        start = self.root
        while True:
            if key == start.key:
                start.val = val
                return
            elif key < start.key:
                if start.left == None:
                    start.left = Node(key, val)
                    self.size += 1
                    return
                start = start.left
            else:
                if start.right == None:
                    ????
                start = start.right
```

Test that you're counting the size correctly -- there should be no asserts in the following:

```python
t = BST()
t.add("B", 3)
assert t.size == 1
t.add("A", 2)
assert t.size == 2
t.add("C", 1)
assert t.size == 3
t.add("C", 4)
assert t.size == 3
```

## Length

Add a special method so that we can take call `len` on a BST.  This should work:

```python
t = BST()
t.add("B", 3)
assert len(t) == 1
t.add("A", 2)
assert len(t) == 2
t.add("C", 1)
assert len(t) == 3
t.add("C", 4)
assert len(t) == 3
```

<details>
<summary>Hint</summary>

A `__len__` method should return `self.size`.
</details>

## Dump

Let's some methods to BST to dump out all the keys and values (note
that "__" before a method name is a hint that it is for internal use
-- methods inside the class might call `__dump`, but code outside the
class probably shouldn't):

```python
    def __dump(self, node):
        if node == None:
            return
        self.__dump(node.right)         # A
        print(node.key, ": ", node.val) # B
        self.__dump(node.left)          # C
        
    def dump(self):
        self.__dump(self.root)
```

Play around with the order of lines A, B, and C above.  Can you
arrange those three so that the output is in ascending alphabetical
order, by key?

Discuss with your neighbour: why not have a `Node.__dump(self)` method
instead of the `BST.__dump(self, node)` method?

<details>
<summary>Answer</summary>

Right now, it is convenient to check at the beginning if `node` is
None.  A receiver (the `self` parameter) can't be None if the
`object.method(...)` syntax is used (you would get the
"AttributeError: 'NoneType' object has no attribute 'method'" error).
We could have a `Node.__dump(self)` method, but then we would need to do the None checks on both `.left` and `.right`, which is slightly longer.
</details>

## Bracket Syntax

Add a special method to BST so that the following code works:

```python
t = BST()
t["B"] = 3
t["A"] = 2
t["C"] = 1
t["C"] = 4
t.dump()
```

<details>
<summary>Answer</summary>

<pre>
    def __setitem__(self, key, val):
        self.add(key, val)
</pre>
</details>

To support lookups, also paste this code in the BST class:

```python
    def __lookup(self, node, key):
        if node == None:
            return None # default
        elif node.key == key:
            return node.val
        elif key < node.key:
            return self.__lookup(node.right, key)
        else:
            assert key > node.key
            return self.__lookup(node.right, key)

    def __getitem__(self, key):
        return self.__lookup(self.root, key)
```

Test it with this code:

```python
t = BST()

# test default
print(t["default"])

# test root
t["B"] = 1
print(t["B"])

# test right child
t["C"] = 2
print(t["C"])

# test update
t["B"] = 3
print(t["B"])
```

The code should print this:

```
None
1
2
3
```

But!  There's a bug in the code we gave you, and none of the tests are
causing the bug to manifest.

1. add some test cases you make up, until you find the bug
2. fix the bug in `__lookup`

<details>
<summary>Hint</summary>

Construct a test case that tries to lookup a value from a node that is the left child of the root.
</details>

## Visualization

Copy/paste the following methods to `BST`, without modification:

```python
    def __graphviz(self, g, node):
        g.node(node.key)
        for label, child in [("L", node.left), ("R", node.right)]:
            if child != None:
                self.__graphviz(g, child)
                g.edge(node.key, child.key, label=label)
    
    def _repr_svg_(self):
        g = Digraph()
        if self.root != None:
            self.__graphviz(g, self.root)
        return g._repr_svg_()
```

## Balance

Run the following:

```python
t = BST()
t["D"] = 9
t["A"] = 8
t["B"] = 7
t["C"] = 6
t["F"] = 5
t["E"] = 4
t["G"] = 3
t
```

You should see something like this:

<img src="part1/1.png" width=300>

Copy/paste the previous example, the modify the order in which letters
are added so that the result looks like this:

<img src="part1/2.png" width=300>

Copy/paste again, and see if you can produce this arrangement by shuffling the lines:

<img src="part1/3.png" width=85>

## Bonus

For those of you looking for a challenge, consider adding a method to
compute the max depth of the tree (the largest number of edges from
the root to a leaf).

Then, perform an experiment where you generate 1000 different trees,
each from 100 key/val pairs that you randomly generate.  Randomly
shuffle the order in which you add the key/val pairs to your BST.

Generate a histogram showing the distribution of max tree depth over
your 1000 trials.
