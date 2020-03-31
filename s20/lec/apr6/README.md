# April 6 Lecture

## 1. Linear Combinations of Columns

### Watch: [20-minute video](https://youtu.be/gv4L1u3lJ1o)

### Practice: Column Subtraction

Paste the following:

```python
import numpy as np

A = np.array([
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

x = np.array([???,???,???]).reshape(-1,1) # TODO
col_dot(A, x)
```

Let's say we want to subtract the third column from the first column
(this is a linear combination!) to get values 97, 198, and 299.

Relpace the `???` parts with numbers to achieve this subtraction.

<details>
    <summary>ANSWER</summary>
    <code>x = np.array([1,0,-1]).reshape(-1,1)</code>
</details>

## 2. Column Space

### Watch: [10-minute video](https://youtu.be/MsOpMnAjB6w)

### Practice: What's in the Space?

Paste this matrix:

```python
A = np.array([
    [5,0,0],
    [0,15,0],
    [0,0,3],
    [-1,-1,-1],
])
A
```

Claim: this column is in the column space of A:

```
array([[15],
       [15],
       [15],
       [-9]])
```

Prove this by finding a linear combination of the columns of A (by
choosing x) that produces the above vector:

```python
x = np.array([3,1,5]).reshape(-1,1)
A.dot(x)
```

The following is NOT in the column space of A:

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

### Watch: [9-minute video](https://youtu.be/QMiZeaUUgc0)

### Practice: Making Bad Matrices

Say a genie appears and gives you a `mystery` function that takes a
row (of size 3) as input and gives back a corresponding output.  The
genie says the function is linear, but does not allow you to see the
code (OK, it's actually below, but play along and don't look at it).

Instead of granting you three wishes, the genie says you can send
three rows as input (`A`) to `mystery` and see the three return values
(`b`).

As a clever numpy user, you run the following to create your own
function, `model`, based on the behavior of `mystery` those three
times.  `model` works just like `mystery`, but you can call it as
often as you like!  (This is the linear algebra equivalent of wishing
for more wishes).

```python
def mystery(row):
    # pretend we can't see this code
    return row[2] - row[0]

A = np.array([
    [1,9,4],
    [1,10,4],
    [1,10,5],
])
b = np.array([[mystery(row)] for row in A])
print("b (outputs):", b)

x = np.linalg.solve(A, b)
print("x coefficients:", x)

def model(row):
    return row.dot(x)

print("model works like mystery!", model(np.array([[1,9,4]])))
print("And we can call it with new values!", model(np.array([[4,5,10]])))
```

This worked out because we tried "good" inputs to `mystery` (which is
not hard, actually -- randmomly chosen `A` values will almost
certainly be "good").

Let's try some "bad" inputs and see how `solve` breaks.  "Bad" inputs
are redundant.  Try the following:

1. change the last row from `[1,10,5]` to `[1,10,4]` (so that it's a repeat of the middle row) and run the code.  Take note of the error.
2. now change the last row from `[1,10,5]` to `[2,19,8]`.  This is not obviously redundant, because all the three rows look different, but it will actually break because row three is a sum of the other two (so sending it to `mystery` provides no new information).

## 4. Projection Matrices

### Watch: [14-minute video](https://youtu.be/wR1nRLL4OQs)

### Practice: Projection

Run the following:

```python
import numpy as np
import pandas as pd
a0 = np.random.normal(20, 5, 30)
a1 = np.random.randint(low=1, high=3, size=30)
noise = np.random.normal(0, 3, 30)
b = a0 * 2 - a1*30 + noise
df = pd.DataFrame({"a0":a0, "a1":a1, "b":b})
df.plot.scatter(x="a0", y="b", c=df["a1"], vmin=0, marker="x")
```

Here, we want to look for the relationship between b (shown on the
y-axis) and a0, a1 (represented as x-axis and color, respectively).

There are two equivalent ways of looking at the problem we face:
1. we're looking for two variables (the coeficients in x by which we multiply a0 and a1), but we have 30 equations (one for each row) that are inconsistent with each other (due to noise)
2. it would not be possible to fit straight lines to the data

Although the `b` column is not a linear combination of the `a0` and
`a1` columns, let's create `p` column that is as close as possible to
`b` while also being a linear combination of the `a` columns.

Complete and run the following (reference the lecture video to get the
formula for the projection matrix):

```python
A = df.values[:, :2]
P = ????
df["p"] = P.dot(df["b"])

ax=df.plot.scatter(x="a0", y="b", c=df["a1"], vmin=0, marker="x")
df.plot.scatter(x="a0", y="p", c=df["a1"], vmin=0, marker="o", ax=ax)
```

In the scatter plot, note that the circles represent the `p` column we
constructed.  Although we don't solve for the coeficients now, note
that visually this now appears to be a tractable problem.
