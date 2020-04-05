# April 10 Lecture (NOT RELEASED YET, IN PROGRESS!)

## 1. Non-Linear Fit

### Watch: [14-minute video](https://youtu.be/R0_WaO71aiE)

### Practice: Polynomial Terms

In the lecture, we added some polynomial terms that were non-linear,
such as x**2 and x**3.  We also added log2(x) and 1/x, which are
non-linear and non-polynomial.

When you only need to deal with polynomials, sklearn has a
preprocessor that will help.  First, let's generate some data:

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression as LR

x = np.random.uniform(0.1,5,100)
noise = np.random.normal(scale=1, size=x.size)
y = (4-x)*(2-x)*(1-x) + noise
df = pd.DataFrame({"y":y, "x":x})
df.head()
```

And plot it...

```python
ax = df.plot.scatter(x="x", y="y")
```

Now, let's import `PolynomialFeatures` and compute x**2, x**3, etc.

```python
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(4, include_bias=False)
columns = ["x"]
arr = poly.fit_transform(df[columns])
poly_df = pd.DataFrame(arr)
poly_df
```

It's a little hard to see the which term is which, because we don't
know the column names!  Pass `columns=poly.get_feature_names(columns)`
to the DataFrame creation call above, so it looks like this:

```python
poly_df = pd.DataFrame(arr, columns=poly.get_feature_names(columns))
```

<img src="poly_df.png" width=400>

Let's fit a line and view the coefficients:

```python
lr = LR()
lr.fit(poly_df, df[["y"]])
lr.coef_, lr.intercept_
```

Now, using those coefficients, let's compute the y values for x=0,
0.1, 0.2, etc., then plot a line through those points:

```python
ax = df.plot.scatter(x="x", y="y", color="0.7")

# compute coords along fit line, then plot it
fit_x = np.arange(0, 5, 0.1).reshape(-1,1)
fit_y = lr.predict(poly.fit_transform(fit_x))
ax.plot(fit_x, fit_y, "red")
```

<img src="fit.png" width=400>

2. Overfitting

## 1. Overfitting

### Watch: [4-minute video](https://youtu.be/3ZPCY0hoHCE)

### Practice: Overcoming Overfitting

One way to overcome overfitting is by collecting more data.  In
general, that make be expensive (image surveying more people for
example).

In the video, we're sampling from a random number generator, so it should be easy.

Run the following, replacing `????` with different sample sizes (e.g.,
10, 20, 50, 100, 1000, 10000) to gain an intuition for how much data
is needed to get a reasonable fit with 15 polynomial terms (c0 + c1*x
+ c2*x**2 + ... + c14*x**14 + c15*x**15).

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression as LR
from sklearn.preprocessing import PolynomialFeatures

# random data
x = np.random.uniform(0.1, 5, ????) # TODO: specify sample size
noise = np.random.normal(scale=1, size=x.size)
y = (4-x)*(2-x)*(1-x) + noise
df = pd.DataFrame({"y":y, "x":x})

# add columns for polynomial terms
poly = PolynomialFeatures(15, include_bias=False)
columns = ["x"]
arr = poly.fit_transform(df[columns])
poly_df = pd.DataFrame(arr, columns=poly.get_feature_names(columns))

# linear regression
lr = LR()
lr.fit(poly_df, df[["y"]])
ax = df.plot.scatter(x="x", y="y", color="0.7", ylim=(-20, 20))

# compute coords along fit line, then plot it
fit_x = np.arange(0, 5, 0.1).reshape(-1,1)
fit_y = lr.predict(poly.fit_transform(fit_x))
ax.plot(fit_x, fit_y, "red")
```
