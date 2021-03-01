# Project 3: Treasure Hunt!

## Corrections/Clarifications
* [Mar 1] `application.py` has been updated.
* [Mar 1] FAQ post [here](https://piazza.com/class/kjomvrz8kyl64u?cid=466)
* [Mar 1] Optional Starter Video: [watch here](https://youtu.be/GuSlUAYvvF8)
* [Feb 28] Tester updated (Tests for go methods have been added)
* [Feb 27] README updated.
* [Feb 27] Tester is now added.

## Overview

In this project you will practice inheritance, graph search, and web
scraping. You'll hand-in a module called `scrape.py`. It will contain
three classes `GraphScraper`, `FileScraper` and `WebScraper`.

Make sure to run the tests (which we plan to release by the weekend!)
before handing in.  During development, we recommend having a
debug.ipynb notebook to make calls to your module.

# Group Part (75%)

For this portion of the project, you may collaborate with your group
members in any way (even looking at working code).  You may also seek
help from 320 staff (mentors, TAs, instructor).  You <b>may not</b>
seek receive help from other 320 students (outside your group) or
anybody outside the course.

### Part 1: `FileScraper` class

Paste the following starter code to your Python module.  Your job is
complete the `go` method in the `FileScraper` class (don't change the
one in `GraphScraper`!), the `bfs_search` method, and the `dfs_search`
method.

The two search methods will call `self.go` to visit nodes.  This will
not work if called on a GraphScraper object directly (because that
class should not have a working `go` method), but `FileScraper` (which
*does* have a `go`) method will inherit them.

```python
import os, zipfile

class GraphScraper:
    def __init__(self):
        self.visited = set()
        self.BFSorder = []
        self.DFSorder = []

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        pass

    def bfs_search(self, node):
        pass

class FileScraper(GraphScraper):
    def __init__(self):
        super().__init__()
        if not os.path.exists("Files"):
            with zipfile.ZipFile("files.zip") as zf:
                zf.extractall()

    def go(self, node):
        pass
```

Note how the constructor of `FileScraper` extracts all the zipped
files to a directory named "Files" for you.  This means you'll be
working with regular files in your code (not the original zip).

The "Files" directory will only contain .txt files, each corresponding
to a node in a directed graph, and each containing four lines,
formatted like this:

1. name of the node
2. names of the children nodes, seperated by spaces
3. "BFS: XXX" where "XXX" is a string
4. "DFS: XXX" where "XXX" is a string

Your task is to implement the `FileScraper` class to scrape the
content of this directory.

The `go` method in the `FileScraper` class should read one of the txt
files and return a list of it's children.  Whenever `go` reads a file,
it should also append the BFS string (line 3 of the file) to the
`BFSorder` list and append the DFS string (line 4 of the file) to the
`DFSorder` list.  For example, you should be able to run the following
in your debug notebook:

```python
from scrape import *
fs = FileScraper()
print(fs.go("1"))
print(fs.go("2"))
print(fs.BFSorder)
print(fs.DFSorder)
```

Expected output:

```
['2', '4']
['1', '3', '5']
['M', 'A']
['C', 'O']
```

Your `bfs_search` (non-recursive) and `dfs_search` (recursive) methods
inherited from `GraphScraper` will perform graph search, somewhat like
the `find` and `find_bfs` methods from the reading, respectively:
https://tyler.caraza-harter.com/cs320/s21/lec/14-graphsearch1/reading.html

There are a few differences, however (your version will be somewhat
simpler overall):

1. we are not looking for a path to any particular destination.  We just want to explore the graph and see what info about nodes we can discover.  This is why we don't have any `dst` parameter.  Our `search` methods will also not need to return anything or do any backtracking.
2. there is not a `Node` class; instead, the methods are in the `GraphScraper` class.  So `self` will no longer refer to a Node object.  Instead, we'll know what node we're on because the name is passed in to the `node` parameter of the search functions
3. also, as there is no `Node` class, we can't use something like `self.children` or `node.children` to learn the nodes of the class.  You should use the `go` method you just wrote for this purpose instead.

We will only ever do one search on your graph object, so there's no
need to ever clear out your `visited` list.

We've arranged the extra info in each file so that the correct search order will lead to recognizable words.  For example, if you run:

```python
fs = FileScraper()
fs.dfs_search("1")
fs.DFSorder
```

You should get `['C', 'O', 'V', 'I', 'D', '1', '9']`.

### Part 2: `WebScraper` class

Be sure to watch this lecture before starting this part:
https://github.com/tylerharter/caraza-harter-com/tree/master/tyler/cs320/s21/lec/17-crawling

You'll be scraping a website implemented as a web application built
using the flask framework (you don't need to know flask for this
project, though you'll learn it soon and get a chance to build your
own website in the next project).  To run it, grab all the relevant
html, csv, and css files.  Grab `application.py` too, and run this on
your VM:

```
python3 application.py
```

Then, open `http://<YOUR-VM-IP>:5000` in your web browser.  It should look like this:

<img src="website.png" width=600>

Each page (under "ENTER THE MAZE") contains information in the form of
a letter.  If you do either a DFS or BFS search through the site and
concatenate the letters from the pages in the order in which they're
visited, you'll get a password.  Use the DFS buttons when doing a DFS
search and the BFS buttons when doing a BFS search.

By performing both searches, you'll get two passwords.  Entering
either correct password on the home page will redirect you to a
different page.

Use selenium to do the scraping.  BeautifulSoup is probably also
helpful, though not required.

```python
class WebScraper(GraphScraper):
    # required
    def	__init__(self, driver=None):
        super().__init__()
        self.driver = driver

    # these three can be done as groupwork
    def go(self, url):
        pass

    def dfs_pass(self, start_url):
        pass

    def bfs_pass(self, start_url):
        pass

    # write the code for this one individually
    def protected_df(self, url, password):
        pass
```

### `go` method

Treat each page as a node, and each hyperlink as a directed
edge. Implement the `go` method such that, each time a page is visited
, the "DFS Click!"  button and "BFS Click!" are clicked to get letters
and append each letter to `self.DFSorder` and `self.BFSorder`
respectively.

### `dfs_pass` method

Use the inherited `dfs_search` method to return the DFS password, which is just all the strings in `DFSorder` joined together (no spaces or other seperation).

### `bfs_pass` method

Like the method above, but use `bfs_search`, and join `BFSorder` instead.

### Manual Debugging

Here is a code snippet you can use as you write your methods to help
test whether they're working:

```python
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# kill previous chrome instance if still around (to conserve memory)
os.system("pkill chrome")

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# TODO: use IP address of your VM
start_url = "http://YOUR_IP_HERE:5000/Node_1.html"

s = WebScraper(driver)
print(s.go(start_url))

dpass = s.dfs_pass(start_url)
print("\nDFS Password", dpass)

bpass = s.bfs_pass(start_url)
print("\nBFS Password", bpass)

s.driver.close()
```

Expected output:

```
['http://YOUR_IP_ADDRESS:5000/Node_2.html', 'http://YOUR_IP_ADDRESS:5000/Node_4.html']

DFS Password BleuSus

BFS Password XÆ_A-12
```

# Individual Part (25%)

You have to do the remainder of this project on your own.  Do not
discuss with anybody except 320 staff (mentors, TAs, instructor).

### Part 3: `protected_df` method

The method should navigate to the home page, enter the password, click
GO, and return a DataFrame based on the page that is loaded.

Note that after clicking a button, there might be a slight delay
before `driver.page_source` reflects the new page.  Consider how you
can use `time.sleep(...)` to reduce the chance that this will happen
on some systems (like our test machine).

You may want to use this function: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html

The method should return the whole DataFrame, even if getting the
whole DataFrame involves clicking a button multiple times to load more
rows.

If `s` is a WebScraper with a driver that has not been closed, this this:

```python
url = "http://YOUR_IP_ADDRESS:5000/"
print(s.protected_df(url, dpass))
```

Should produce this:

```
   ID   Latitude   Longitude Access Code                          Description
0   1  43.089034  -89.416128  983kbsdfk1              Picnic Point in Madison
1   2  38.105507  126.910613  37461983fd               Silver Beach in Hawaii
2   3  65.044901  -16.712836  jnjsd238yf  Shore of a Volcanic Lake in Iceland
3   4  48.860945    2.335773  7733hhfsdf                  The Louvre in Paris
4   5  37.434183 -122.321990  ksjfn21213      Redwood forest in San Francisco
5   6  51.180315   -1.829659  348219389f                 Stonehenge in the UK
6   7  27.987586   86.925002  njsg1hywov                 Mt. Everest in Nepal
7   8  43.070010  -89.409450  8wbd1vy29a          Quick Trip on Monroe Street
```
