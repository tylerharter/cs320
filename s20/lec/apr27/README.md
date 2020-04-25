# April 27 Lecture

## 1. Categorical Inputs

### Watch: [19-minute video](https://youtu.be/KDzTIlWe6HY)

### Practice: Water Temperature

Let's explore the relationship between water temperature and wave height.

Download the data:

```
wget https://github.com/tylerharter/cs320/raw/master/s20/lec/apr27/waves.csv
```

Read it in:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("waves.csv")
df = df[(df["Wave Period"] > 0) & (df["Wave Height"] > 0)]
df.head()
```

Complete the following to create a plot similar to the one in the
video, with water temperature on the x-axis and wave height on the
y-axis:

```python
fig, axes = plt.subplots(2, 3, figsize=(12, 8), sharex=True, sharey=True)
plt.subplots_adjust(hspace=0.3)
axes = list(axes.reshape(????)) # flatten to one dimension, as long as necessary

beach_names = sorted(set(df["Beach Name"]))
for b in beach_names:
    ax = axes.???? # remove first from list, put to ax
    ax.set_title(b)
    beach_df = ???? # get only those rows where beach name is b
    beach_df.plot.scatter(x="Water Temperature", y="Wave Height", 
                          color="k", alpha=0.05, ax=ax)
```

<details>
    <summary>ANSWER</summary>
    <code>-1</code>, <code>pop(0)</code>, and <code>df[df["Beach Name"] == b]</code>.
</details>

Do you see any obvious evidence of faulty temperature data on any of the beaches?

<details>
    <summary>ANSWER</summary>
    <img src="rainbow.png">
</details>

## 2. One-Hot Encoding

### Watch: [16-minute video](https://youtu.be/73S3ERmZqjs)

### Practice: Missing Categories

Create some simple DataFrames, noting that `df2` has one fruit that `df1` does not:

```python
df1 = pd.DataFrame({"fruit": ["apple", "banana", "kiwi"]})
df2 = pd.DataFrame({"fruit": ["apple", "apple", "banana"]})
df1
```

Complete the following to fit the data to `df1`, then transform `df2`:

```python
from sklearn.preprocessing import OneHotEncoder

oh = OneHotEncoder()
oh.fit(df1)
data = oh.transform(df2).???? # TODO: convert from spares array to regular array
pd.DataFrame(data, columns=oh.get_?????_names())
```

<details>
    <summary>ANSWER</summary>
    <code>toarray()</code> and <code>feature</code>
</details>

You should get something like this:

<img src="expected.png">

What happens if we fit to the data with the missing kiwi, then try to
transform the data that does have kiwi?  Try swapping `df1` and `df2`
in the above example to find out.

<details>
    <summary>ANSWER</summary>
    You should get <code>ValueError: Found unknown categories ['kiwi'] in column 0 during transform</code>
</details>

To get around this, pass `handle_unknown="ignore"` to the creation of the OneHotEncoder, like this:

```python
oh = OneHotEncoder(handle_unknown="ignore")
```

Now, you won't get an error, but note that there will only be columns
for the categories that showed up in the fitted data.  The row for
kiwi in the transformed output will have all zeros, because it is not
an apple and not a banana.  The columns are determined at fitting
time.

## 3. Visualizing Predictions

### Watch: [9-minute video](https://youtu.be/VL4FiVzlbQM)
