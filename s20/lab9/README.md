# Lab 9: Writing Zip Files and Making Geographic Maps

In this lab, you'll get practice creating files inside .zip files.
This will require learning new ways to convert strings to bytes, and
an exploration of compression options to save space.

We'll also guide you through creating an informative map of Europe
using geopandas (a packages based on pandas that we'll introduce in
more detail in the next lecture).

You'll use both these new skills for P4.

## Part 1: Creating Zips

In this example, you'll learn how to create your own .zip file in
Python code.  There are two reasons to zip things:

1. bundle a bunch of files into one big file that can easily be shared
2. compress the data to save space

### Hello World and Common Bugs

Writing a file inside a zip file is a three step process:

1. open the zip file
2. open a file inside the zip file
3. write to that inner file

Try pasting and running this code, which tries to do that, but has two small bugs:

```python
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED

with ZipFile("new.zip") as zf:
    with zf.open("inside.txt", "w") as f:
        f.write("hello world!\n")
```

**Bug 1:** `FileNotFoundError: [Errno 2] No such file or directory: 'new.zip'`

When writing files inside a .zip, both opens need the "w" mode. So add
it to the opening of new.zip (like `with ZipFile("new.zip", "w") as
zf`) and try again.

**Bug 2:** `TypeError: a bytes-like object is required, not 'str'`

This is progress, we're got past the line where the we were getting an
exception before, and are now crashing on the `.write` line (be sure
to notice such progress when you're debugging).

Files can be opened in either text mode (meaning strings will be
written to them) or binary mode (meaning bytes will be written to
them).  A normal call to `open(...)` that you've used many times
defaults to text mode, but a call to `zf.open(...)` unfortunately
opens in binary mode.

Fortunately, it's easy to convert our string to bytes using an
encoding, such as "utf-8" (by definition, this conversion is what
encoders do).  Try it with a simple example first:

```python
s = "hello"
b = bytes(s, encoding="utf-8")
print(b)
```

Now let's see if this can fix our original attempt.  Try this code:

```python
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED

with ZipFile("new.zip", "w") as zf:
    with zf.open("inside.txt", "w") as f:
        f.write(bytes("hello world!\n", encoding="utf-8"))
```

Let's see if it worked.  In a terminal, go to the directory where you
created the .zip file, and run this:

```
unzip -p new.zip inside.txt
```

You should see "hello world!".  Note, if this were a much longer file,
you might only want to see the beginning, in which case you might run
(`unzip -p new.zip inside.txt | head`).

### CSVs inside Zips

Try the following buggy code:

```python
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
import csv

with ZipFile("new.zip", "w") as zf:
    with zf.open("inside.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y"]) # header
        writer.writerow(["1", "2"])
        writer.writerow(["3", "4"])
```

You should get `TypeError: a bytes-like object is required, not 'str'`
-- note, this is the exact same exception we saw before!

Do you see the tricky situation we're in?  The `writerow` call wants
to write strings, but `f` is open in binary mode and expects bytes.

We solved this before by adding a little code to convert our string to
bytes, but now we have no such opportunity.  `writerow` is directly
writing strings to `f`, without giving as an opportunity to easily
insert our own conversion.

The solution is the `io.TextIOWrapper`.  These wrappers take in
strings strings and automatically convert them to bytes beneath.
Let's squeeze this in between the `csv.writer` and `f`:

```python
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from io import TextIOWrapper
import csv

with ZipFile("new.zip", "w") as zf:
    with zf.open("inside.csv", "w") as raw:
        with TextIOWrapper(raw) as f:
            writer = csv.writer(f)
            writer.writerow(["x", "y"]) # header
            writer.writerow(["1", "2"])
            writer.writerow(["3", "4"])
```

Go back to the terminal and verify we produced what we wanted:

```
unzip -p new.zip inside.txt
```

### Compression

When opening a new ZipFile, you can decide the compression mode.
Enabling compression (aka "deflation") will save you space, but it
will often slower to read/write the data.

Copy/paste the following function that writes a table (5 million rows)
to a CSV in a .zip:

```python
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from io import TextIOWrapper
import csv, time

def test_compression(zip_name, compression_mode):
    with ZipFile(zip_name, "w", compression=compression_mode) as zf:
        with zf.open("inside.csv", "w") as raw:
            with TextIOWrapper(raw) as f:
                writer = csv.writer(f)
                writer.writerow(["x", "y"]) # header
                for i in range(5000000):
                    writer.writerow([str(i*2), str(i*2+1)])
```

Note that we can pass in a compression mode such as `ZIP_DEFLATED`
(compressed) or `ZIP_STORED` (not compressed).  Let's compare these
two options:

```python
t0 = time.time()
test_compression("deflated.zip", ZIP_DEFLATED)
t1 = time.time()
print(t1-t0)
```

Creating the compressed file took 10.66 seconds on my VM.  Let's try non-compressed:

```python
t0 = time.time()
test_compression("regular.zip", ZIP_STORED)
t1 = time.time()
print(t1-t0)
```

That took 7.36 seconds on my VM (hopefully it was slightly faster for
you too).

Now let's compare the file sizes of the zip files.  In the terminal,
run this `ls -lh *.zip` ("l" means "list mode" and "h" means "human
readable").  You'll probably see something like this:

```
-rw-rw-r-- 1 trh trh 23M Mar 21 19:11 deflated.zip
-rw-rw-r-- 1 trh trh 81M Mar 21 19:11 regular.zip
```

Although it took a few extra seconds to create deflated.zip, we see
the file only uses 23 MB (megabytes), in contrast to the 81 MB used by
regular.zip.

## Part 2: geopandas practice

We'll be talking more about geopandas in the next lecture, but for
now, we'll guide you through some steps to make a map.

If you haven't already, you need to install some things to make maps:

```
pip3 install geopandas shapely descartes
```

And this:

```
sudo apt install python3-rtree
```

Let's say you want to plot a map of Europe, showing major cities and
shading countries by popluation.  Past+run the following:

```python
import geopandas
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))

eu = world[world["continent"] == "Europe"]
ax = eu.plot(column="pop_est")
geopandas.sjoin(cities, eu).plot(ax=ax)
```

It should look like this:

<img src="map-bad.png">

Can't see much there!  We'll walk you through a series of changes to
make it look like this much-better version:

<img src="map-good.png">

Re-generate the map after each step so you can see the result of your
changes.

### Step 1: Latitude/Longitude Limits

At the end of the cell, paste these calls:

```python
ax.set_xlim(-25, 45)
ax.set_ylim(30, 80)
```

### Step 2: Country Styling

Let's use the "Oranges" color map, put a light gray border around
countries, and increase the color size.  In the above snippet, change
the `ax = eu.plot(...)` line to this:

```python
ax = eu.plot(column="pop_est", cmap="Oranges", edgecolor="0.8", figsize=(8,8))
```

### Step 3: City Styling

Let's use small black markers for cities by passing `color` and
`markersize` to the second `.plot` call:

```python
geopandas.sjoin(cities, eu).plot(ax=ax, color="black", markersize=3)
```

### Step 4: Removing Axes

Although there are exceptions, axes are often less useful for maps
than other plots, so add this to turn them off:

```python
ax.set_axis_off()
```

### Summary

If you got stuck above, here are all the changes together:

```python
import geopandas
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))

eu = world[world["continent"] == "Europe"]
ax = eu.plot(column="pop_est", cmap="Oranges", edgecolor="0.8", figsize=(8,8))
geopandas.sjoin(cities, eu).plot(ax=ax, color="black", markersize=3)
ax.set_xlim(-25, 45)
ax.set_ylim(30, 80)
ax.set_axis_off()
```