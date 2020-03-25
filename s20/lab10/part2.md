# Categorizing by Range

Suppose we have a list of values and a list of non-overlapping ranges.
We want to count how many values fall in each range.

Paste this solution:

```python
from collections import defaultdict

def count_by_range_v1(values, ranges):
    counts = defaultdict(int)
    for v in values:
        for r in ranges:
            if r[0] <= v <= r[1]: # line A
                counts[r] += 1
    return counts
```

Try it:

```python
count_by_range_v1(values=[1, 11, 30, 35, 90, 85, 2],
                  ranges=[(1, 10), (11, 50), (51, 100)])
```

Look good?  Let's try another more complicated version:

```python
def count_by_range_v2(values, ranges):
    values.sort() # eliminate this?
    ranges.sort() # eliminate this?

    r_idx = 0
    r = ranges[r_idx]

    counts = defaultdict(int)
    for v in values:
        while v > r[1]:
            r_idx += 1 # line C
            if r_idx == len(ranges):
                return counts # all remaining values past last range
            r = ranges[r_idx]
    
        # we know that v <= r[1] since we stopped looping above
        if r[0] <= v: # line B
            counts[r] += 1
    return counts
```

Test that one too.  You ought ought to get the same result.

Now assume that `N=len(values)` and `M=len(ranges)`.  Think carefully
about the code, then answer the following:

How many times will line A execute?

<details>
    <summary>ANSWER</summary>
    <code>M*N</code>
</details>

How many times will line B execute, at most?

<details>
    <summary>ANSWER</summary>
    <code>N</code>
</details>

How many times will line C execute, at most?

<details>
    <summary>ANSWER</summary>
    <code>M</code>
</details>

What is the time complexity of version 1?

<details>
    <summary>ANSWER</summary>
    <code>O(M*N)</code>
</details>

Note that version 2 needs to sort `values` and `ranges` before it can
do its counting.  Let's say we deleted those two lines, and just made
a restriction that anybody calling the function should only pass in
pre-sorted lists.  What would the complexity of version 2 be then?

<details>
    <summary>ANSWER</summary>
    <code>O(M+N)</code>
</details>

Food for thought: how does this relate to the `country` command for P4?
