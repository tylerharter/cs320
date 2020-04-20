# April 22 Lecture

## 1. Regression vs. Classification

### Watch: [15-minute video](https://youtu.be/hL0IDe6xP6w)

### Practice: Simplification

Download `df.csv`.  Then paste and complete the following:

```python
import pandas as pd
import numpy as np

df = pd.read_csv("df.csv")

def get_row(i):
    return df.loc[i, "x1":"one"].values.reshape(1,-1).astype(float)

vec2 = np.array([[ 1.37239431],
                 [-1.16675093],
                 [-1.32467119],
                 [ 6.59925245]])

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def classification_model_v1(row):
    return sigmoid(row @ vec2).round().astype(bool)

def classification_model_v2(row):
    return ????

eq = classification_model_v1(df.loc[:, "x1":"one"]) == classification_model_v2(df.loc[:, "x1":"one"])
eq[0].value_counts()
```

Can you find something for `????` that makes `classification_model_v2` behave just like `classification_model_v1`, but doesn't need `sigmoid` or `astype`?

<details>
    <summary>ANSWER</summary>
<code>row @ vec2 >= 0</code>  This works because `sigmoid(0)` is 0.5.  The benefit of the more complicated version with `sigmoid` is easily differentiable, making gradient descent a useful tool for finding the logistic regression coefficients.
</details>

## 2. Training and Testing

### Watch: [12-minute video](https://youtu.be/Jm6De1kvhm0)

Generate some random data, then split it into test/train data:

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

features = 1
rows = 50
x = np.random.uniform(0,10,rows)
df = pd.DataFrame({f"x{i}": x+np.random.normal(size=x.size, scale=5) for i in range(features)})
df["y"] = x > 5
train, test = train_test_split(df, test_size=0.5)
train.head()
```

How well does it doe on the training and test data?

```python
lr = LogisticRegression(penalty="none")
lr.fit(train.iloc[:, :-1], train["y"])
lr.score(train.iloc[:, :-1], train["y"]), lr.score(test.iloc[:, :-1], test["y"])
```

Evaluating on a test dataset that's separate from the training dataset
helps us better gauge the performance of the model, especially when
the model might be overfitting the training data.

There is a greater risk for overfitting the training data when the
number of features is large relative to the number of rows.  Increase
`features = 50` above to observe this problem.

What scores do both get now?  You probably observe perfect scores on
the training data, but that doesn't mean anything because the model
essentially memorized the oddities of that data.  It doesn't do so
great on the test data.

Note that we specifically disabled penalties with `penalty="none"`.
We won't go into detail here about what this parameter means, but it
is used to avoid overfitting.  Remove `penalty="none"`, then see
whether the model does better on the training data.

## 3. Pipelines

### Watch: [13-minute video](https://youtu.be/oI3edPIvUjQ)

`LogisticRegression` doesn't do very well when the scale of different
columns varies a lot.  To see this, generate some random data:

```python
x1 = np.random.uniform(0,1,100)
x2 = np.random.uniform(8000,9000,100)
y = x1 * 1000 + x2 > 9000
df = pd.DataFrame({"x1":x1, "x2":x2, "y":y})
df.head()
```

Note that there is no noise in this data!

See how well LogisticRegression does:

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

train, test = train_test_split(df)
lr = LogisticRegression()
lr.fit(train[["x1", "x2"]], train["y"])
lr.score(test[["x1", "x2"]], test["y"])
```

Not so great, considering there is no noise, huh?

We can re-scale the data using `StandardScaler` in a pipeline.
`StandardScaler` subtracts the mean from each columns (leaving a new
mean of zero), then divides each column by its standard deviation.

Complete the pipeline to re-scale before the data reached a
LogisticRegression (you don't need to pass any argument to the
`StandardScaler`):

```python
pipe = Pipeline([
    ("std", ????),
    ("lr", ????),
])
```

<details>
    <summary>ANSWER</summary>
<code>StandardScaler()</code> and <code>LogisticRegression()</code>
</details>

Call `fit` and `score` as we did for `lr` earlier, but instead of
`lr`, use your `pipe` object.  A little better, eh?
