# Part 1 Hints

## Length

```python
    def __len__(self):
        if self.next == None:
            # base case: I'm the only Node!  Length must be 1
            return 1
        else:
            # recursive case: total length is the length of next plus 1
            return len(self.next) + ????
```

## Representation

```python
    def __repr__(self):
        if self.next == None:
            return repr(self.val)
        else:
            return repr(self.val)+","+repr(self.next)
```

## Indexing

```python
    def __getitem__(self, idx):
        if idx == 0:
            # base case
            return self.????
        else:
            # recursive case
            return self.next[idx-1]
```

## Negative Indexing

```python
    def __getitem__(self, idx):
        if ????: # check if we have a negative index
            idx = len(self) + idx

        ...
```

## Append

```python
    def append(self, val):
        last_node = self
        while last_node.next != None:
            last_node = last_node.next
        last_node.next = Node(????)
````
