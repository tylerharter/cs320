# Lab 14: Decision Boundaries

We've learned two kinds of supervised learning: regression and
classification.

Visualizing a regression model (like LinearRegression) is
often straightforward: just draw a fit line.

How can we visualize a classification model (like LogisticRegression)?
In this lab, you'll learn how to visualize decision boundaries.  In
the end, it will look like this:

<img src="deg3.png" width=400>

# Example Data

Generate and plot some scatter data:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = np.random.uniform(-3, 3, 200)
y = 1 - x + np.random.normal(0, size=x.shape)
z = ((0 < x-y/3) & (x-y/3 < 2.8)) | (x < -2.8)

df = pd.DataFrame({"x":x, "y":y, "z":z})
ax = df.plot.scatter(x="x", y="y", c=df["z"], vmin=-1)
```

<img src="scatter.png" width=400>

If we wanted to find model the relationship between the y and x
variables, what kind of model do we need?

<details>
    <summary>ANSWER</summary>
    Regression.  y is continuous.
</details>

If we wanted to find model the relationship between z (represented by
the color of the points) and inputs x and y, what kind of model do we
need?

<details>
    <summary>ANSWER</summary>
    Classification.  z is categorical.
</details>

## Regression

Fit a line and view:

```python
from sklearn.linear_model import LinearRegression
ax = df.plot.scatter(x="x", y="y", c=df["z"], vmin=-1)

lr = LinearRegression()
lr.fit(df[["x"]], df["y"])
x = np.array(ax.get_xlim())
y = lr.predict(x.reshape(-1, 1))
ax.plot(x, y, c="red")
```

<img src="fit.png" width=400>

## Classification

Let's train a pipeline using a LogisticRegression to separate the
black from gray points.

To visualize this, we'll do the following:

1. train our model
2. create a regular scatter plot
3. break up the plot area into a grid of points
4. determine how the model predicts each of these possible points
5. use `plt.contourf` to smoothly show the decisions (and the boundary between them)

Please do all steps in the same cell (just keep adding the code we
show to the end)!

If you run into trouble, you can see the whole code
[here](solution.md).  But don't look at that unless you're really,
really stuck. :)

### Step 1: training

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("poly", PolynomialFeatures(1)), # degree 1 does nothing
    ("std", StandardScaler()),
    ("lr", LogisticRegression()),
])
pipe.fit(df[["x", "y"]], df["z"])
```

### Step 2: scatter

Run it:

```python
df.plot.scatter(x="x", y="y", c=df["z"], vmin=-1)
```

### Step 3: meshgrid

At the end of your cell, add this:

```python
x, y = np.meshgrid(np.arange(-3, ax.get_xlim()[1], 0.01),
                   np.arange(ax.get_ylim()[0], ax.get_ylim()[1], 0.01))
x, y
```

`meshgrid` breaks up the space into two matrices covering the entire
space (with `0.01` granularity, in this case).  The first one has the
x coords of each point (which is why each column contains only one
distinct number).  The second one contains the y coords of each point.

Add this to the end of your cell:

```python
xy = np.hstack((x.reshape(-1,1), y.reshape(-1,1)))
xy
```

The reshaping arranges each as a vertical column, and the hstack puts
them side-by-side in a matrix.

### Step 4: predicting each point

The advantage of the shape of `xy`: this is in proper form to feed
into a model.  Let's do that!

```python
z = pipe.predict(xy).reshape(x.shape)
z
```

### Step 5: visualizing decision boundaries

Ok, now we can plot the decision boundaries (using `alpha=0.1` for
semi-transparency) on top of scatter points, adding the following in
the same cell:

```python
plt.contourf(x, y, z, alpha=0.1, cmap="binary")
```

You should get this:

<img src="deg1.png" width=400>

## Improvements

Clearly, a straight line can't separate the gray from the black very
well.  Adjust the pipeline to fit 2nd-degree polynomials
(`PolynomialFeatures(1)` should be changed to
`PolynomialFeatures(2)`).  Now you'll get this:

<img src="deg2.png" width=400>

Finally, try allowing 3rd-degree polynomials to separate the points:

<img src="deg3.png" width=400>