# Clustering for Color Segmentation

An image is a matrix of colors.  Each cell, called a *pixel*, contains
a red, green, and blue value (mixing these can create any color).  If
we re-organize an image into a table such that we have one row per
pixel and and red, green, and blue columns, then we can perform
clustering on that table.  The result will inform us about the main
colors in the image.

This page has an image of the WI capital that we'll use: https://en.wikipedia.org/wiki/Madison,_Wisconsin.  Download a resized version of it:

```
wget https://raw.githubusercontent.com/tylerharter/cs320/master/s21/lab13/capital.jpg
```

Run the following to read and view the image:

```python
from matplotlib import pyplot as plt
img = plt.imread("capital.jpg")
plt.imshow(img)
```

<img src="capital.jpg" width=200>

`img` is three dimensional: row, column, color amounts.  Check it's
`.shape`, then use `.reshape` fit it into a DataFrame like the one we
described above:

```python
import pandas as pd
rgb = pd.DataFrame(????, columns=["red", "green", "blue"])
rgb
```

<details>
    <summary>ANSWER</summary>
    <code>img.reshape(-1, 3)</code>
</details>

Use KMeans clustering to identify 4 centroids for the colors:

```python
from sklearn.cluster import KMeans
km = ????(n_clusters=4)
km.????(rgb)
```

Look at `km.cluster_centers_`; this contains the four resulting 4
centroids (each on a row, each containing three color amounts).

Convert the centroid values to ints and place them in a DataFrame
called centroids that has the same columns as `rgb`.

<details>
    <summary>ANSWER</summary>
    <code>pd.DataFrame(km.cluster_centers_.astype(int), columns=rgb.columns)</code>
</details>

Reshape centroids.values so that we have 1 row by 4 columns by 3
colors, then pass the result to `imshow`:

`plt.imshow(????)`

<details>
    <summary>ANSWER</summary>
    <code>centroids.values.reshape(1, 4, 3)</code>
</details>

The result should look like this:

<img src="4colors.png">

```python
km = KMeans(n_clusters=4)
km.fit(img.reshape(????))
plt.imshow(km.cluster_centers_.reshape(????).astype(int))
```

<details>
    <summary>ANSWER</summary>
    <code>-1,3</code> and <code>1,4,3</code>
</details>

How accurate is the image if we redraw it using only those 4 colors?
Complete the following using `int`, `img.shape`, `labels_`, and
`cluster_centers_` (not necessarily in that order).

```python
img2 = km.????.astype(????)[km.????].reshape(????)
plt.imshow(img2)
```
