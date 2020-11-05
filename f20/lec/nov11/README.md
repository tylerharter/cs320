# Nov 11 Lecture

## 1. Linear Combinations of Columns

### Watch: [17-minute video](https://youtu.be/wWSx2tMke_E)

### Practice: Column Subtraction

Paste the following:

```python
import numpy as np

X = np.array([
    [100,10,3],
    [200,10,2],
    [300,10,1]
])

def col_dot(M, v):
    col_sum = np.zeros((len(M), 1))
    for col_idx in range(M.shape[1]):
        col = M[:, col_idx:col_idx+1] * v[col_idx,0]
        #print(col, "\n")
        col_sum += col
    return col_sum

c = np.array([???,???,???]).reshape(-1,1) # TODO
col_dot(X, c)
```

Let's say we want to subtract the third column from the first column
(this is a linear combination!) to get values 97, 198, and 299.

Relpace the `???` parts with numbers to achieve this subtraction.

<details>
    <summary>ANSWER</summary>
    <code>c = np.array([1,0,-1]).reshape(-1,1)</code>
</details>

## 2. Column Space

### Watch: [11-minute video](https://youtu.be/32AdszqQvvM)

### Practice: What's in the Space?

Paste this matrix:

```python
X = np.array([
    [5,0,0],
    [0,15,0],
    [0,0,3],
    [-1,-1,-1],
])
X
```

Claim: this column is in the column space of X:

```
array([[15],
       [15],
       [15],
       [-9]])
```

We can prove this by finding a linear combination of the columns of X.
We do so by multiplying the columns of X by the coefficients in the
following vector c.  Try it:

```python
c = np.array([3,1,5]).reshape(-1,1)
X @ c
```

The following is NOT in the column space of X:

```
array([[5],
       [15],
       [3],
       [1]])
```

Can you make an argument why it's not?

<details> <summary>ANSWER</summary> To get a positive (1) in
    that last position, we would need to multiply at least one of the
    columns by a negative.  But any way we might do this would force
    us to have a negative in the 1st, 2nd, or 3rd position, which we
    don't see. </details>

## 3. When `np.linalg.solve` fails

### Watch: [14-minute video](https://youtu.be/4qMXkKW8XnQ)

### Practice: Making Bad Matrices

Say a genie appears and gives you a `mystery` function that takes a
row (of size 3) as input and gives back a corresponding output.  The
genie says the function is linear, but does not allow you to see the
code (OK, it's actually below, but play along and don't look at it).

Instead of granting you three wishes, the genie says you can send
three rows as input (`X`) to `mystery` and see the three return values
(`y`).

As a clever numpy user, you run the following to create your own
function, `model`, based on the behavior of `mystery` those three
times.  `model` works just like `mystery`, but you can call it as
often as you like!  (This is the linear algebra equivalent of wishing
for more wishes).

```python
def mystery(row):
    # pretend we can't see this code
    return row[2] - row[0]

X = np.array([
    [1,9,4],
    [1,10,4],
    [1,10,5],
])
y = np.array([[mystery(row)] for row in X])
print("y (outputs):", y)

c = np.linalg.solve(X, y)
print("c coefficients:", c)

def model(row):
    return row @ c

print("model works like mystery!", model(np.array([[1,9,4]])))
print("And we can call it with new values!", model(np.array([[4,5,10]])))
```

This worked out because we tried "good" inputs to `mystery` (which is
not hard, actually -- randomly chosen `X` values will almost
certainly be "good").

Let's try some "bad" inputs and see how `solve` breaks.  "Bad" inputs
are redundant.  Try the following:

1. change the last row from `[1,10,5]` to `[1,10,4]` (so that it's a repeat of the middle row) and run the code.  Take note of the error.
2. now change the last row from `[1,10,5]` to `[2,19,8]`.  This is not obviously redundant, because all the three rows look different, but it will actually break because row three is a sum of the other two (so sending it to `mystery` provides no new information).
