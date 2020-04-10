# April 8 Lecture

## 1. Fit Lines

### Watch: [16-minute video](https://youtu.be/uCyV-tVLgDU)

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
Value ~= 4.012921950803952*JerseyNumber + -34.424892877423986*Age + -1550.7687191703085*PreferredFootInt + 294.15939084161107*Wage + 1319.4229840508806
```

The trick here is how to deal with foot, since it's "Left" or "Right",
not a number.  You might consider encoding "Left" as 0 and "Right" as
1, with something like this: `df["PreferredFootInt"] = (df["PreferredFoot"] == "Right").astype(int)`

Look closely at the coefficients.  Does the magnitude of the
JerseyNumber and Wage coefficients match your intuition?  Are right
footed or left footed players likely to have higher net worth?

## 2. Loss Functions

### Watch: [11-minute video](https://youtu.be/f6v7WCJQ2tA)

### Practice: General Functions

Complete the following code:

```
def euclidean_dist(df, col1, col2):
    return ????

def mean_squared_error(df, col1, col2):
    return (euclidean_dist(df, col1, col2) ** 2) / len(df)
```

For reference, we computed the euclidean distance
between the `b` and `p1` columns during the video using
`edist = ((df["b"] - df["p1"]) ** 2).sum() ** 0.5`.

To test your code, let's compute a `p` column in `df` (from the part 1
practice), then compare that to the `Value` column :

```python
df["p"] = r.predict(df[columns])

print("euclidean dist:", euclidean_dist(df, "Value", "p"))
print("MSE:", mean_squared_error(df, "Value", "p"))

df
```

You should get this:

```
euclidean dist: 6791.905876854667
MSE: 2306499.2720026486
```

## 3. Storage

Not related to linear algebra, but wanted to teach how to increase
disk size...

### Watch: [17-minute video](https://youtu.be/5OuasxWJT40)

# Remember!

Please record that you finished this lecture: https://forms.gle/z9oCk4BzvVjdN1aZ6