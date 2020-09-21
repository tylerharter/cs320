# Zip Files

As you deal with bigger datasets, those datasets will often be
compressed.  Compressed means that the format takes advantage of
patterns and redundancy in data to same a bigger file in less space.

For example, say you have a string like this: "HAHAHAHAHAHAHAHAHAHA".
You should imagine inventing a notation for representing that string
with fewer characters (maybe something like "HA{x10}").

Zip is one common compression format.  In addition to compressing
files, .zips often bundle multiple files together.  In the past, you
would have run `unzip` in the terminal before starting to write your
code.  However, it is also possible to directly read the contents of a
`.zip` file in Python.  Doing so is often more convenient; the code
may also quite possibly be faster.

## Generating a .zip

To create an `example.zip` file, run the following (don't worry,
understanding this particular snippet isn't expected for this lab):

```python
import pandas as pd
from zipfile import ZipFile, ZIP_DEFLATED
from io import TextIOWrapper

with open("hello.txt", "w") as f:
    f.write("hello world")

with ZipFile("example.zip", "w", compression=ZIP_DEFLATED) as zf:
    with zf.open("hello.txt", "w") as f:
        f.write(bytes("hello world", "utf-8"))
    with zf.open("ha.txt", "w") as f:
        f.write(bytes("ha"*10000, "utf-8"))
    with zf.open("bugs.csv", "w") as f:
        pd.DataFrame([["Mon",7], ["Tue",4], ["Wed",3], ["Thu",6], ["Fri",9]],
                     columns=["day", "bugs"]).to_csv(TextIOWrapper(f), index=False)
```

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
with ZipFile('example.zip') as zf:
    for info in zf.infolist():
        print(info)
```

Let's print off the size and compression ratio (uncompressed size divided by compressed size) of each file:

```python
with ZipFile('example.zip') as zf:
    for info in zf.infolist():
        orig_mb = info.file_size / (1024**2) # there are 1024**2 bytes in a MB
        ratio = info.file_size / info.compress_size
        s = "file {name:s}, {mb:.3f} MB (uncompressed), {ratio:.1f} compression ratio"
        print(s.format(name=info.filename, mb=orig_mb, ratio=ratio))
```

Take a minute to look through -- what file is largest?  What is its
compression ratio?

The compression ratio is the original size divided by the compressed
size, so bigger means more savings.  `ha.txt` contains "hahahahaha..."
(repeated 10 thousand times), which is highly compressible.

As practice, compute the overall compression ration (sum of all
uncompressed sizes divided by sum of all compressed sizes) -- it ought
to be about 216.

## Binary Open

Ok, forget zips for a minute, and run the following:

```python
with open("hello.txt", "r") as f:
    data1 = f.read()

with open("hello.txt", "rb") as f:
    data2 = f.read()

print(type(data1), type(data2))
```

What type does `f.read()` return if we use "r" for the mode?  What
about "rb"?

The "b" stands for "binary" or "bytes", so we get back type `bytes`.
If we open in text mode (the default), as in the first open, the bytes
automatically get translated to strings, using some encoding (like
"utf-8") that assigns characters to byte-represented numbers.

Run this:

```python
from io import TextIOWrapper
```

`TextIOWrapper` objects "wrap" file objects are used to convert bytes
to characters on the fly.  For example, try the following:

```python
with open("hello.txt", "rb") as f:
    tio = TextIOWrapper(f)
    data3 = tio.read()
print(type(data3))
```

Even though we open in binary mode, we get a string thanks to
`TextIOWrapper`!  You can think of the example where we read into
`data1` as a shorthand for what we did to get `data3`.

## Reading Files

A ZipFile has a method named `open` that works a lot like the `open`
function you're familiar with.  A ZipFile is a context manager, and so
is the object returned by `ZipFile.open(...)`, so we'll end up with
nested `with` statements to make sure everything gets closed up
properly.  Let's take a look at the compressed schedule file:

```python
with ZipFile('example.zip') as zf:
    with zf.open("hello.txt", "r") as f:
        print(f.read())
```

Woah, why do we get `b'hello world'`?  For regular files, "r" mode
defaults to reading text, but for files inside a zip, it defaults to
binary mode, so we got back bytes.

TextIOWrapper saves the day:

```python
with ZipFile('example.zip') as zf:
    with zf.open("hello.txt", "r") as f:
        tio = TextIOWrapper(f)
        print(tio.read())
```

With regular files, TextIOWrapper is a bit useless (why not just open
with "r" instead of "rb"?), but for zips, it is crucial.

## Pandas

Pandas can read a DataFrame even from a binary stream.  So you can can do this:

```python
with ZipFile('example.zip') as zf:
    with zf.open("bugs.csv") as f:
         df = pd.read_csv(f)
df
```
