# Nov 13 Lecture

## 1. Projection Matrices

### Watch: [18-minute video](https://youtu.be/T5SLKSKrMC8)

### Practice: Projection

Run the following:

```python
import numpy as np
import pandas as pd
x0 = np.random.normal(20, 5, 30)
x1 = np.random.randint(low=1, high=3, size=30)
noise = np.random.normal(0, 3, 30)
y = x0 * 2 - x1*30 + noise
df = pd.DataFrame({"x0":x0, "x1":x1, "y":y})
df.plot.scatter(x="x0", y="y", c=df["x1"], vmin=0, marker="x")
```

Here, we want to look for the relationship between y (shown on the
y-axis) and x0, x1 (represented as x-axis and color, respectively).

There are two equivalent ways of looking at the problem we face:
1. we're looking for two variables (the coefficients in x by which we multiply x0 and x1), but we have 30 equations (one for each row) that are inconsistent with each other (due to noise)
2. it would not be possible to fit straight lines to the data

Although the `y` column is not a linear combination of the `x0` and
`x1` columns, let's create `p` column that is as close as possible to
`y` while also being a linear combination of the `a` columns.

Complete and run the following (reference the lecture video to get the
formula for the projection matrix):

```python
X = df.values[:, :2]
P = ????
df["p"] = P.dot(df["y"])

ax=df.plot.scatter(x="x0", y="y", c=df["x1"], vmin=0, marker="x")
df.plot.scatter(x="x0", y="p", c=df["x1"], vmin=0, marker="o", ax=ax)
```

In the scatter plot, note that the circles represent the `p` column we
constructed.  Although we don't solve for the coeficients now, note
that visually this now appears to be a tractable problem.

## 2. Fit Lines

### Watch: [23-minute video](https://youtu.be/94YtWZOHIaY)

### Practice: Multiple Linear Regression

In this example, you'll do a Multiple Linear Regression, which just
means that we're trying to find a relationship between the response
variable and multiple explanatory variables.

We'll try to find what predicts the net worth of a Soccer/Football
player.

Paste and run the following (data adapted from [here](https://www.kaggle.com/karangadiya/fifa19/data)):

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

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
df.dtypes
```

Now, do a regression over Jersey Number and Age:

```python
r = LinearRegression()
columns = ["JerseyNumber", "Age"]
r.fit(df[columns].values, df["Value"].values.reshape(-1,1))
print("Coef:", r.coef_)
print("Intercept:", r.intercept_)
```

Can we construct a nice formula from those values?  Complete the following, using `columns` and `reg.intercept_[0]`:

```python
def formula(reg, columns):
    rv = ""
    for i in range(len(columns)):
        rv += "{}*{} + ".format(reg.coef_[0,i], "????")
    rv += str("????")
    return rv

print("Value ~= " + formula(r, columns))
```

You ought to get output like this:

```
Value ~= -27.27295205695321*JerseyNumber + 33.788003740974744*Age + 923.5388822632224
```

You should be a skeptical of those results.  Can Jersey number really
affect net worth?  Is 20 rows really enough to learn a pattern?

Try adapting the code to get a formula that includes preferred foot
and wage, to get an equation like this:

```
Value ~= -26.788038968540928*JerseyNumber + 24.34001562860506*Age + -1265.349183600262*PreferredFootInt + 1781.6739153865974
```

The trick here is how to deal with foot, since it's "Left" or "Right",
not a number.  You might consider encoding "Left" as 0 and "Right" as
1, with something like this: `df["PreferredFootInt"] = (df["PreferredFoot"] == "Right").astype(int)`

Look closely at the coefficients.  Does the magnitude of the
JerseyNumber and Wage coefficients match your intuition?  Are right
footed or left footed players likely to have higher net worth?

## 3. Loss Functions

### Watch: [11-minute video](https://youtu.be/XIyDrcHSc0E)
