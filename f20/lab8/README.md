# Lab 8: Web

In this part, you'll build a simple Flask game, called "Guess that
Function!".  You'll also learn `curl`; `curl` is like `cat`, but for
sending web requests instead of reading files.

We'll practice some parts in a notebook, then copy to a Flask application.

If you get confused about the directions about what to add to your
flask application, you can always peek at our complete version in
[solution.py](solution.py), but of course it's better practice to try to
figure it out on your own first.

## StringIO

In a notebook, paste+run the following:

```python
from io import StringIO
f = StringIO()
f.write("hello\n")
f.write("world!")
s = f.getvalue()
print(s)
```

A `StringIO` instance is what is known as a file-like object in
Python, meaning you can read/write to it (the "IO" part stands for
input/output).

This is handy when you want a string (which you can get with
`.getvalue()`) but you're dealing with a Python module that only works
with file objects, as in the next part.

## SVG

The SVG (Scalable Vector Graphics) files are common on the web, and
can easily be mixed in with HTML (without even needing a separate
file).

In a notebook, let's try generating an SVG file.

```python
from matplotlib import pyplot as plt
from io import StringIO

def get_ax():
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    return ax

ax = get_ax()

# "save" to a string in the SVG format
f = StringIO()
ax.get_figure().savefig(f, format="svg")
svg_data = f.getvalue()

print(svg_data)
```

You should see something like this:

```
<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<!-- Created with matplotlib (https://matplotlib.org/) -->
<svg height="576pt" version="1.1" viewBox="0 0 576 576" width="576pt" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
 <defs>
  <style type="text/css">
*{stroke-linecap:butt;stroke-linejoin:round;}
  </style>
 </defs>
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 576 
L 576 576 
L 576 0 
L 0 0 
z
" style="fill:#ffffff;"/>
  </g>
  ...
```

Note that the above looks a bit like HTML; indeed, it can be inserted
directly into the middle of HTML.

## SVG in Flask

Start a new Flask app in a file named `guess.py`, pasting the following
(which is adapted from the example you just did in the notebook).

```python
from matplotlib import pyplot as plt
from flask import Flask, request
from io import StringIO

app = Flask(__name__)

def get_ax():
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    return ax

@app.route('/plot.svg')
def show_plot():
    ax = get_ax()

    # "save" to a string in the SVG format
    f = StringIO()
    ax.get_figure().savefig(f, format="svg")
    svg_data = f.getvalue()

    html = "<html><body><h1>Guess that function</h1>{}</body></html>"
    return html.format(svg_data)

# Be sure this if statement stays as the last thing in your .py!
if __name__ == '__main__':
    app.run(host="0.0.0.0")
```

Now, in a terminal, connect via SSH, and run the following:

```
python3 guess.py
```

It should look something like this:

<img src="run.png" width=400>

Now, ask whoever you're doing the lab with to go to
`http://your-ip:5000/plot.svg`, replacing `your-ip` with your VMs
public IP address.

They should see something like this:

<img src="browser.png" width=600>

## Guess Route

Add a function to your `guess.py` file, something like the following:

```python
def f(x):
    return -abs(x) # TODO: change this to your favorite mathematical function
```

Make `f` some sort of mathematical function, importing from the `math`
module if you like.  It doesn't matter what the function is.  The
"game" is that people will try to guess it.

Now, let's add a route so people can upload (POST) their guesses to
the server.  Paste the following in `guess.py` and restart the server
(kill it with `CTRL-C` before running `python3 guess.py` again).

```python
@app.route('/guess', methods=["POST"])
def guess():
    parts = request.get_data(as_text=True).split(",")
    x = float(parts[0])
    y = float(parts[1])
    actual = f(x)
    if actual == y:
        return "perfect\n"
    return "f({}) is {}, not {}\n".format(x, actual, y)
```

If you were to go to `http://your-ip:5000/guess` in your browser, you'll
see "Method Not Allowed", since web browsers generally use GETs (not
POSTs) when you first visit a page.

## POSTing with `requests`

Remember the `requests` module we learned in CS 220/301?  We can use
that to make guesses.  First import it:

```python
import requests
```

Then use it to send POST requests to your partners' web servers to see
if you can figure out their functions (`other-ip` should be whatever
they tell you their VM's IP address is):

```python
r = requests.post("http://other-ip:5000/guess", data="3,4")
r.raise_for_status()
r.text
```

You should get some output like this:

```
'f(3.0) is -3.0, not -4.0'
```

Or, if you're lucky:

```
'perfect'
```

Make a few guesses until you think you know their function, then check
with them.

## POSTing with `curl`

From another terminal, SSH to your VM, and run the following (again
replacing `other-ip` with that of your partners' IP addresses) --
watch the upper/lower case!

```
curl -X POST http://other-ip:5000/guess -d "3,4"
```

Here, `curl` is sending HTTP requests, using the `POST` method with
request body containing "3,4" (the part after `-d`).

`curl` is a quick and easy way to send web requests.  If you want to
do a GET request, it's even simpler:

```
curl http://other-ip:5000/plot.svg
```

That should dump out all the code for the SVG image.

## Plotting Guesses

Let's record guesses then plot them in `/plot.svg`.  Import pandas and
create a DataFrame for guesses (this code goes in `guess.py`):

```python
import pandas as pd

guesses_df = pd.DataFrame()
```

Now let's record guesses -- add the following to the `guess` function,
before the return statement:

```python
    idx = len(guesses_df)
    guesses_df.loc[idx, "x"] = x
    guesses_df.loc[idx, "y"] = y
    guesses_df.loc[idx, "actual"] = actual
```

Also, let's scatter the guesses and correct answers in the `show_plot` function:

```python
    if len(guesses_df):
        ax = guesses_df.plot.scatter(x="x", y="actual", c="black", s=60, ax=ax, zorder=1, label="actual")
        ax = guesses_df.plot.scatter(x="x", y="y", c="red", s=20, ax=ax, zorder=2, label="guess")
```

Restart your server, then ask your partner(s) to send you some
guesses, with `requests` or `curl`.  Then have somebody refresh the
`/plot.svg` page.  It ought to look something like this (red-on-black
dots represent correct guesses):

<img src="guess.png" width=600>

## Optional Fun

Ideas for making "Guess that Function!" even more fun:

* can you randomly pick a function when the server starts?
* can you give users scores, based on their average error?
* can you have a way to reset the guesses?
