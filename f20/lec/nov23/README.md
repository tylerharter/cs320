# Nov 23 Lecture

## 1. Nearest Neighbour

### Watch: [37-minute video](https://youtu.be/OBIJ-Hbx2fs)

### Practice:

In the demo, we did k-means in 2 dimensions.  You can also do it in 3 or more.

Do some imports and generate some 3-dimensional data:

```python
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

count = 100
df = pd.DataFrame({"x1": np.random.normal(size=count),
                   "x2": np.random.normal(size=count),
                   "x3": np.random.normal(size=count),})
df["y"] = "orange"
noise = np.random.normal(size=count, scale=0.2)
df.loc[df["x1"]<noise, "y"] = "lightblue"
df.loc[:4, "y"] = "black"
```

Now plot it in 3D:

```python
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(df["x1"], df["x2"], df["x3"], c=df["y"])
```

The first five rows (black) have not been categorized yet (as blue or
orange).

Fit the NearestNeighbor classifier from lecture to the last 95 rows, then use it to fill in the first five unknown rows:

```python
class NearestNeighbor(BaseEstimator, ClassifierMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y):
        self.memX_, self.memy_ = check_X_y(X, y)
        self.classes_ = unique_labels(y)
        return self
    
    def predict(self, X):
        check_is_fitted(self)
        X = check_array(X)
        if X.shape[1] != self.memX_.shape[1]:
            raise ValueError("train/test feature mismatch")
        y = []
        for i,row1 in enumerate(X):
            best_dist = None
            for j,row2 in enumerate(self.memX_):
                dist = ((row1 - row2) ** 2).sum() ** 0.5
                if best_dist == None or dist < best_dist:
                    best_dist = dist
                    best_y = self.memy_[j]
            y.append(best_y)
        return np.array(y)

nn = NearestNeighbor()
nn.fit(df.loc[5:, ["x1", "x2", "x3"]], df.loc[5:, "y"])
df.loc[:4, "y"] = nn.predict(df.loc[:4, ["x1", "x2", "x3"]])
```

Plot it again.  Does it seem to have chosen reasonable colors for the
unknown rows?

## 2. sklearn Transformers

### Watch: [10-minute video](https://youtu.be/kvEqgpUJaVc)
