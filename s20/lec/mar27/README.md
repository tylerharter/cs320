# March 27 Lecture

## 1. Correction About geopandas Types

### Watch: [4-minute video](https://youtu.be/4l09oHbwOg4)

## 2. Shapefiles

### Watch: [13-minute video](https://youtu.be/5Q5gxEZSg_Q)

### Practice: Map of United States

For practice, you'll download and manipulate a shapefile to create a
map of the United States.

Go to the US Census page here and use `wget` to download the zipped
shapefile named `cb_2018_us_state_20m.zip` to your VM:

https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html

Now, create a map using this:

```python
import geopandas
us = geopandas.read_file("zip://states.zip")
us.plot(color="orange", edgecolor="k")
```

<img src="us-bad.png" width=400>

Pretty unreadable, huh?  If we draw Alaska, Hawaii, and Puerto Rico
separately from the continental US, we can get a more readable map,
like this:

<img src="us-good.png" width=600>

First, let's split the GeoDataFrame to four parts:

```python
us.set_index("STUSPS", drop=False, inplace=True)
continent = us[~us["STUSPS"].isin(["AK", "HI", "PR"])]
ak = us.loc["AK":"AK"]
hi = us.loc["HI":"HI"]
pr = us.loc["PR":"PR"]
```

Now, copy/paste the following to a cell create four areas where we can
plot:

```python
fig = plt.figure()
gs = fig.add_gridspec(5, 3)
ax1 = fig.add_subplot(gs[:3, :])
ax2 = fig.add_subplot(gs[3, 0])
ax3 = fig.add_subplot(gs[3, 1])
ax4 = fig.add_subplot(gs[3, 2])
```

<img src="grid.png" width=400>

Add the following to the same cell where you pasted the last code to
draw the four groups of states:

```python
continent.plot(color="orange", edgecolor="k", ax=ax1)
ak.plot(color="orange", edgecolor="k", ax=ax2)
hi.plot(color="orange", edgecolor="k", ax=ax3)
pr.plot(color="orange", edgecolor="k", ax=ax4)
```

At this point, you'll notice two remaining problems:

1. the axes add clutter
2. Alaska wraps around to the Eastern hemisphere, making it difficult to plot

Solve both these problems by adding the following to your cell that
does the plotting:

```python
ax2.set_xlim(-180, -120)
for ax in fig.axes:
    ax.axis("off")
```

## 3. High Resolution Images

### Watch: [4-minute video](https://youtu.be/JGdUoyn74ZQ)

## 4. Shapely Shapes: Venn Diagrams Example

### Watch: [22-minute video](https://youtu.be/2JXq37PanQI)

### Practice: Make a `venn` function

Complete the following function:

```python
def venn(a_label, a_set, b_label, b_set):
    pass
```

You should be able to call it like this:

```python
venn("pets", {"dogs", "snakes", "birds"}, 
     "mammals", {"dogs", "cats", "whales", "gorillas"})
```

To get a plot Venn like this:

<img src="venn.png" width=300>

For your convenience, here is the code from the lecture video to adapt
for your function:

```python
from shapely.geometry import Polygon, Point
from matplotlib import pyplot as plt
from descartes import PolygonPatch

a_set = {1, 2, 3}
b_set = {3, 4, 5, 6, 7, 8}

qa = len(a_set.difference(b_set))
qb = len(b_set.difference(a_set))
qab = len(a_set.intersection(b_set))
q_max = max(qa, qb, qab)

fig,ax = plt.subplots(figsize=(3,2))
ax.set_xlim(0,3)
ax.set_ylim(0,2)

c1 = Point(1, 1).buffer(1)
ax.text(1, 2, "A", size=20, va="bottom", ha="center")
c2 = Point(2, 1).buffer(1)
ax.text(2, 2, "B", size=20, va="bottom", ha="center")
A = c1.difference(c2)
B = c2.difference(c1)
AB = c1.intersection(c2)

for quantity, area in [(qa, A), (qb, B), (qab, AB)]:
    percent_of_max = quantity / q_max
    bg_color = (1-percent_of_max)*0.6 + 0.4
    ax.add_artist(PolygonPatch(area, facecolor=str(bg_color)))
    ax.text(area.centroid.x, area.centroid.y, quantity, size=16)
plt.axis("off")
```

Solution [here](part4solution.md).