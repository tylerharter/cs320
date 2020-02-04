# Part 3: Merge Sort

Merge sort is a recursive strategy for sorting.  The strategy is
simple:

1. check if the list has length < 2 -- if so, it's already sorted (base case)
2. otherwise, split the list in two equal parts
3. run merge sort on each half to get two smaller sorted lists
4. merge the two sorted lists into one bigger sorted list

To get the idea, step through this visualization of the algorithm,
using list size 8 (yes, there are 96 steps, but it's worth it):

https://opendsa-server.cs.vt.edu/embed/mergesortAV

Now let's run some actual Python code.  There will be two functions,
`merge` and `merge_sort`.

## merge(L1, L2)

Start by copying `merge` to your notebook

```python
def merge(L1, L2):
    rv = []
    idx1 = 0
    idx2 = 0

    while True:
        done1 = idx1 == len(L1)
        done2 = idx2 == len(L2)

        if done1 and done2:
            return rv

        choose1 = False
        if done2:
            choose1 = True
        elif not done1 and L1[idx1] < L2[idx2]:
            choose1 = True

        if choose1:
            rv.append(L1[idx1])
            idx1 += 1
        else:
            rv.append(L2[idx2])
            idx2 += 1

    return rv
```

Test it out with some simple cases, like this (also make up at least
one case yourself):

```python
merge([2, 4, 7, 8], [1, 3, 5, 6])
```

To better understand how the function is behaving, try adding this
print inside the loop, after all the other code:

```python
print(rv, " <= ", L1[idx1:], L2[idx2:])
```

## merge_sort(L)

Now copy the `merge_sort` function.  `merge_sort` calls itself
recursively on the two halves of its own list, then merges the two
sorted halves with `merge`:

```python
def merge_sort(L):
    if len(L) < 2:
        return L
    mid = len(L) // 2
    left = L[:mid]
    right = L[mid:]
    left = merge_sort(left)
    right = merge_sort(right)
    rv = merge(left, right)
    return rv
```

Give it a try with a simple test case:

```python
merge_sort([2, 4, 7, 8, 1, 3, 5, 6])
```

To better understand what is going on, add this print statement, right before the return in `merge_sort` (also, remove the print you added earlier to `merge`):

```python
print(rv, " <= ", left, right)
```

## Complexity

Merge sort has `O(N log N)` complexity.  This is actually the
theoretical best for general sorting.  Remember that selection sort in
class was `O(N**2)`, which is worse.

Let's see what an `O(N log N)` curve looks like by counting steps
inside the `merge(...)` function.  First, the steps variable global:

```python
def merge(L1, L2):
    global steps
    ...
```

Then count steps inside the loop:

```python
    while True:
        steps += 1
    ...
```

Finally, paste and run the following, to discover the relationship
between input size and amount of work that must be done:

```python
work_curve = pd.Series() # N => steps

L = []
for N in range(100):    
    steps = 0 # reset steps

    merge_sort(L)
    work_curve.loc[N] = steps

    L.append(N)
    
ax = work_curve.plot.line()
ax.set_xlabel("N")
ax.set_ylabel("Steps")
```

You should see something like this:

<img src="part3/1.png">

As you can see, there's a slight curve.  `O(N log N)` is worse than
`O(N)`, but it's also MUCH better than `O(N**2)`.
