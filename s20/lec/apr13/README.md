# April 13 Lecture

## 1. Factoring Matrices with SVD

### Watch: [9-minute video](https://youtu.be/z5c_U_48oKk)

### Practice: Matrix Factors

Imagine a matrix A had been factored into parts with this:

```python
u,s,vt = np.linalg.svd(A)
```

Then, somebody gave you the three parts, but not the original matrix A
-- paste+run the following:

```python
import numpy as np

u = np.array([[-0.21483724,  0.88723069,  0.40824829],
              [-0.52058739,  0.24964395, -0.81649658],
              [-0.82633754, -0.38794278,  0.40824829]])
s = np.array([16.84810335261421, 1.06836951455471, 0])
vt = np.array([[-0.47967118, -0.57236779, -0.66506441],
               [-0.77669099, -0.07568647,  0.62531805],
               [-0.40824829,  0.81649658, -0.40824829]])
```

Do the multiplications (replacing `????`) necessary to reconstruct the
original matrix, then display it, rounded to 2 decimal places:

```python
A = ????
np.round(A, 2)
```

<details>
    <summary>ANSWER</summary>
    <code>
A = (u*s)@vt
    </code>
</details>

<details>
    <summary>ANSWER (alternate solution)</summary>
    <code>
A = (u*s).dot(vt)
    </code>
</details>

## 2. Eignenvectors and Eigenvalues

### Watch: [10-minute video](https://youtu.be/BIQSACxN7fU)

### Practice: Eigenvector Check

Paste+run:

```python
A = np.array([[4, 1, 7],
              [1, 4, 3],
              [7, 3, 4]])

v1 = np.array([0.68777769, 0.4381872, 0.69928217]).reshape(-1,1)
v2 = np.array([-0.1017017, -0.77186858, 0.29665168]).reshape(-1,1)
v3 = np.array([0.6627402, 0.20526185, -0.72016873]).reshape(-1,1)
v4 = np.array([0.89036881, -0.78460023, 0.30786775]).reshape(-1,1)

A.dot(v1) / v1
```

See how the output is this?

```python
array([[11.75419509],
       [10.35715557],
       [12.76471   ]])
```

This means `v1` is not an eigenvector.  Otherwise, the dot product of
`A` by `v1` would change the scale of each element by an equal amount.

Try the other vectors (`v1` through `v4`) until you identify the
eigenvector.  What is it's eigenvalue?

<details>
    <summary>ANSWER</summary>
v3 is an eigenvector, with eigenvalue -3.29685518.
</details>

## 3. Principal Component Analysis

### Watch: [9-minute video](https://youtu.be/wxqIxBDDb3A)

### Practice: PCA of Soccer/Football Stats

Paste+run:

```python
import numpy as np
import pandas as pd

rows = [['M. Dupé', 1, 25, 'Right', 8.0, 900.0],
       ['N. Fernández', 26, 18, 'Right', 1.0, 450.0],
       ['P. Kalambayi', 30, 18, 'Right', 1.0, 130.0],
       ['P. McNair', 17, 23, 'Right', 22.0, 2300.0],
       ['G. Bojanich', 23, 33, 'Right', 6.0, 425.0],
       ['A. Kofler', 31, 31, 'Right', 3.0, 325.0],
       ['N. Lavanchy', 14, 24, 'Right', 3.0, 600.0],
       ['O. Al Khalaf', 8, 21, 'Right', 3.0, 240.0],
       ['J. Sills', 21, 31, 'Right', 7.0, 600.0],
       ['B. Fox', 12, 20, 'Right', 1.0, 230.0],
       ['S. Smith', 9, 20, 'Left', 4.0, 450.0],
       ['E. Ocansey', 28, 20, 'Left', 5.0, 1600.0],
       ['F. Kostić', 10, 25, 'Left', 16.0, 10500.0],
       ['M. Ullmann', 13, 22, 'Left', 3.0, 1000.0],
       ['R. Taylor', 9, 30, 'Left', 4.0, 625.0],
       ['N. Vikonis', 34, 34, 'Left', 7.0, 2700.0],
       ['J. Aguirre', 29, 21, 'Left', 1.0, 575.0],
       ['J. Konings', 25, 20, 'Left', 1.0, 500.0],
       ['J. Raitala', 22, 29, 'Left', 3.0, 700.0],
       ['A. Taylor', 3, 31, 'Left', 3.0, 425.0]]
df = pd.DataFrame.from_records(rows, columns=["Name", "JerseyNumber", "Age", "PreferredFoot", "Wage", "Value"])
df["PreferredFootInt"] = (df["PreferredFoot"] == "Right").astype(int)
df = df[["JerseyNumber", "Age", "Wage", "Value", "PreferredFootInt"]]
df
```

How many principal components are necessary to capture at least 99% of
the variance?  Run the following to find out (notice we only care
about the absolute values of the eigenvalues in `s` -- we can ignore
the other return values with `_`):

```python
_,s,_ = np.linalg.svd(df)
s = np.array(sorted(np.abs(s), reverse=True))
s.cumsum() / s.sum()
```

<details>
    <summary>ANSWER</summary>
2 components, because 1 only gets us to 0.98439685, but two components together gets us to 0.99521466.
</details>

## 4. sklearn PCA

### Watch: [12-minute video](https://youtu.be/st1LfyVggZI)

### Practice: Scatter Plot

Sometimes, it is useful to identify the single most important
principal component.  Reducing multiple columns down to one will allow
us to produce a scatter plot (and perhaps perform a regression).

Generate some data:

```python
import numpy as np
import pandas as pd

x = np.random.uniform(0,100,size=50) # hidden
y = 20 - x # want to predict this
x1 = 2*x
x2 = 10-3*x
x3 = 20+x
df = pd.DataFrame({"x1":x1, "x2":x2, "x3":x3, "y":y})
noise = np.random.normal(scale=10, size=df.shape)
df += noise
df.head()
```

Note that we don't have an `x` column in our DataFrame.  We do have
`x1` through `x3` columns that all vary together, and a related `y`
variable.

Can we reduce the 3 x variables back to single variable, a pc1 column
(Principal Component 1)?

Try it:

```python
from sklearn.decomposition import PCA
pca = PCA(????)
df["pc1"] = pca.fit_transform(df[[????]])
df.head()
```

<details>
    <summary>ANSWER</summary>
Pass in <code>1</code> for the first <code>????</code> and Pass in <code>"x1", "x2", "x3"</code> for the second <code>????</code>
</details>

Now you have one variable to plot y against:

```python
df.plot.scatter(x="pc1", y="y", color="red")
```

Was that a good idea, or are we missing patterns by collapsing three
variables to one?  Let's check:

```python
pca.explained_variance_ratio_
```

A number close to 1 means that we're capturing most of the
co-variance.  Looks like we're good!