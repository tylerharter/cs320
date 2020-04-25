# April 27 Lecture

## 1. Categorical Inputs

### Watch: [19-minute video](https://youtu.be/KDzTIlWe6HY)

### Practice: Water Temperature

Let's explore the relationship between water temperature and wave height.

Download the data:

```
wget ????
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
    <code>-1</code>, <code>.pop(0)</code>, and <code>df[df["Beach Name"] == b]</code>.
</details>

Do you see any obvious evidence of faulty temperature data on any of the beaches?

<details>
    <summary>ANSWER</summary>
    <img src="rainbow.png">
</details>

## 2. One-Hot Encoding

### Watch: [16-minute video](https://youtu.be/73S3ERmZqjs)

### Practice: ????

## 3. Visualizing Predictions

### Watch: [9-minute video](https://youtu.be/VL4FiVzlbQM)
