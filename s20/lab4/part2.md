# Part 2: Zip Files

For project 2 (probably not released by the time you're doing this
lab) will involve analyzing many different files inside of one big zip
file.  In the past, you would have run `unzip` in the terminal before
starting to write your code.  However, it is also possible to directly
read the contents of a `.zip` file in Python.  Doing so is often more
convenient; the code may also quite possibly be faster.

## Downloading the .zip file

You can download it using wget, like this:

```
wget https://github.com/tylerharter/cs320/raw/master/s20/p2/mmt_gtfs.zip
```

You could run the above in a terminal.  Alternatively, if you start a
cell with `!` in Jupyter, you can run terminal commands on your
virtual machine, without ever leaving your notebook.  Let's try that:

```
! wget https://github.com/tylerharter/cs320/raw/master/s20/p2/mmt_gtfs.zip
```

After you downloaded, you probably ought to delete that cell.  It will
be super SLOW to re-download every time you re-run your code.

## ZipFile

We can access the file by using the `ZipFile` type, imported from the `zipfile` module:

```python
from zipfile import ZipFile
```

ZipFiles are context managers, much like file objects.  Let's try
creating one using `with`, then loop over info about the files inside
using [this
method](https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.infolist):

```python
with ZipFile('mmt_gtfs.zip') as zf:
    for info in zf.infolist():
        print(info)
```

Let's print off the size and compression ratio (uncompressed size divided by compressed size) of each file:

```python
with ZipFile('mmt_gtfs.zip') as zf:
    for info in zf.infolist():
        orig_mb = info.file_size / (1024**2) # there are 1024**2 bytes in a MB
        ratio = info.file_size / info.compress_size
        s = "file {name:s}, {mb:.3f} MB (uncompressed), {ratio:.1f} compression ratio"
        print(s.format(name=info.filename, mb=orig_mb, ratio=ratio))
```

Take a minute to look through -- what file is largest?  Which has the best compression ratio?

As practice, compute the overall compression ration (sum of all
uncompressed sizes divide by sum of all compressed sizes) -- it ought
to be a little less than 6.

## Reading Files

A ZipFile has a method named `open` that works a lot like the `open`
function you're familiar with.  A ZipFile is a context manager, and so
is the object returned by `ZipFile.open(...)`, so we'll end up with
nested `with` statements to make sure everything gets closed up
properly.  Let's take a look at the compressed schedule file:

```python
with ZipFile('mmt_gtfs.zip') as zf:
    with zf.open("calendar.txt") as f:
        print(f.read())
```

That looks like a CSV file, with Window's style line endings (`\r\n`)!
Let's use pandas to see it better:

```python
import pandas as pd

with ZipFile('mmt_gtfs.zip') as zf:
    with zf.open("calendar.txt") as f:
        df = pd.read_csv(f)

df.head()
```

Which services are offered on Saturdays?  Let's find out:

```python
df[df["saturday"] == 1]
```

# Other Bus Files

You should also take a look at these other CSV files inside `mmt_gtfs.zip` that you'll need to understand for P2:

* routes.txt
* stops.txt
* trips.txt
* stop_times.txt

A little terminology: a *route* is a path that the buses regularly
take, like route 80, etc.  The place where a bus picks up or drops off
passengers is called a *stop*.  It's common for multiple routes to use
the same stop.

A *trip* is a path that a particular bus takes, from stop to stop,
usually in service of a route.  There are usually many trips per day
in service of a particular route (because different people ride at
different times).  The *stop_times* data indicates when the buses are
supposed to arrive at each stop when on a particular trip.
