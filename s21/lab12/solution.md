# Solution

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LogisticRegression

# fit logistic regression model
pipe = Pipeline([
    ("poly", PolynomialFeatures(3)),
    ("std", StandardScaler()),
    ("lr", LogisticRegression()),
])
pipe.fit(df[["x", "y"]], df["z"])

# points
df.plot.scatter(x="x", y="y", c=df["z"], vmin=-1)

# decision boundaries
x, y = np.meshgrid(np.arange(-3, ax.get_xlim()[1], 0.01),
                   np.arange(ax.get_ylim()[0], ax.get_ylim()[1], 0.01))
xy = np.hstack((x.reshape(-1,1), y.reshape(-1,1)))
z = pipe.predict(xy).reshape(x.shape)
plt.contourf(x, y, z, alpha=0.1, cmap="binary")
pipe.score(df[["x", "y"]], df["z"])
```