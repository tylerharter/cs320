# UNDER CONSTRUCTION (don't start yet)

# Project 3: Publishing Data

## Corrections/Clarifications

* none yet

## Overview


## Setup

pip3 install Flask, lxml, html5lib

# Requirements

## Data

You get to choose the dataset for this project.  Find a CSV you like
somewhere, then download it as a file named "data.csv".

The file should have between 10 and 1000 rows and between 3 and 15
columns.  Feel free to drop rows/columns from your original data
source if necessary.

Leave a comment in your `main.py` about the source of your data.

## Pages

Your web application should have four pages:
* index.html
* browse.html
* api.html
* donate.html

You should set up flask routes so that going to `http://your-ip:port/`
returns the content from `index.html` (this hopepage is the only
special case).

Going to `http://your-ip:port/browse.html` should returns the content
for `browse.html`, and similarly for the other pages.

You should put whatever content you think makes sense on the pages.
Just make sure that they all start with an `<h1>` heading, giving the
page a title.

Also, the index.html page should have hyperlinks to all the other
pages.

## Browse

The `browse.html` page should show an HTML table with all the data
from `data.csv`.  Don't truncate the table (meaning we want to see all
the rows).  Don't have any other tables on this page, so as not to
confuse our tester.

Hint: look into `_repr_html_` for DataFrames.

## API

## Donations

## Ratings

