# Project 2: Decision Trees and Bias

## Corrections/Clarifications

* Feb 19: add an example for SimplePredictor
* Feb 16: tips for getting started: https://youtu.be/Ws1B8Wz4sEg
* Feb 15: edited bias_test part of tester.py
* Fed 13: fix bias_test result in README
* Feb 12: clarified `loans()` method and `name`,`reader` in `Bank` class. And, added an Expected output for `get_bank_names`. clarified how to interpret `action_taken` more.
* Feb 11: clarified how to interpret `action_taken`

FAQ Post [HERE](https://piazza.com/class/kjomvrz8kyl64u?cid=333)

## Overview

In this project, you'll learn about zip files, modules, object
oriented programming, and trees.

You'll create a new `tree.py` file from scratch; that's the only file
you need to hand in (though it is probably useful to also create a
notebook to use your module for debugging purposes).

You will end up implementing the following classes and functions.

```python
class ZippedCSVReader
class Loan
class Bank
def get_bank_names
class SimplePredictor
class DTree
def bias_test
```

## Background: Redlining

Sadly, there is a long history of lending discrimination based on race
in the United States.  In some cases, lenders have literally drawn red
lines on a map around certain neighbourhoods where they would not
offer loans, based on the racial demographics of those neighbourhoods
(read more about redlining here:
https://en.wikipedia.org/wiki/Redlining).  If you're interested as to
how redlining can still be seen today, here is an article discussing
similar behaviors seen in the insurance industry:
https://www.propublica.org/article/minority-neighborhoods-higher-car-insurance-premiums-white-areas-same-risk

In 1975, congress passed the Home Mortgage Disclosure Act (HDMA), to
bring more transparency to this injustice
(https://en.wikipedia.org/wiki/Home_Mortgage_Disclosure_Act).  The
idea is that banks must report details about loan applications and
which loans they decided to approve.  In this project, we'll
be analyzing HDMA data from Wisconsin, Illinois, and Louisiana:
https://www.consumerfinance.gov/data-research/hmda/historic-data/.

As data scientists, a real concern we must consider is whether our
models show bias.  If we train our models to mimic human behavior,
will they pickup on human bias?  If we don't base our models on
sufficient data, will they overgeneralize?  In this project, we'll be
providing several files describing decision trees.  Decisions trees
are a kind of model that can output things like approve/deny on a
row-by-row basis.  Your job will be to write Python code to load and
run the decision trees.  At least one of them is racially biased, and
you'll be asked to write a function that exposes this.

## Testing

Most of you will be more familiar with writing a Jupyter notebook for
a project.  Writing a module is a bit different: you're creating a
module with a collections of functions/classes that other people could
use in their projects.

Using those functions/classes isn't part of this project, but you'll
need to do that anyway in order to troubleshoot your code.  We
recommend creating a `debugging.ipynb` notebook (for your own
purposes, not to turn in) that imports your module and uses some of
the classes/functions.  You might do something like this:

```python
from tree import *
%load_ext autoreload
%autoreload 2
```

This imports everything from your tree.py file so that you can write
snippets of code that use it.  The `%` lines automatically reload your
module if you change it (well, it usually works -- you'll need to
occasionally run "Kernel Restart & Run All" when it doesn't).

To run our `tester.py`, you'll need to download the .zip files,
tester.py, and expected.json. tester.py will test whether each class
and class methods are properly implemented.  This is helpful in terms
of grading, but is not an easy way to troubleshoot your code as you go
(your `debugging.ipynb` will be better for that).

We strongly recommend against copying code back and forth between the
notebook and .py file throughout the development process.  It's a
habit that will slow you down in the long run (it's better to
comfortable directly writing code in your .py).

# Group Part (75%)

For this portion of the project, you may collaborate with your group
members in any way (even looking at working code).  You may also seek
help from 320 staff (mentors, TAs, instructor).  You <b>may not</b>
seek receive help from other 320 students (outside your group) or
anybody outside the course.

## `ZippedCSVReader` Class

We're providing `loans.zip`, `mini.zip`.  This class
will help your other code access the data.  Here are a couple examples
of how the class is instantiated:

```python
tree_reader = ZippedCSVReader("trees.zip")
data_reader = ZippedCSVReader("mini.zip")
```

After the above call, it should be possible to see a list of files via a `paths` attribute, like this:

```python
print(data_reader.paths) # in alphabetical order!
```

For this, you can refer to lab3 part2 (https://github.com/tylerharter/cs320/blob/master/s21/lab3/part2.md).

Your ZippedCSVReader will have two methods to help people access the
data inside a zip file: `load_json` and `rows`.  Both accept an
argument specifying the name of a file inside the zip.  `load_json`
uses the `json` module parse the specified .json file inside the zip,
and returns a dict.  `rows` works on .csv files; it returns a list of
dicts corresponding to each row (hint: look into how csv.DictReader
works).  Furthermore, if no file name is passed to `rows`, then it
will read all files ending with ".csv" contained inside the zip,
returning a big list of dicts corresponding to the records in all the
CSV files (the rows of CSV files that are alphabetically earlier will
appear earlier in this list).

Example usage:

```python
tree = tree_reader.load_json("simple.json")
print(tree.keys())

dict_list = data_reader.rows("wi.csv")
print()
print(dict_list[0])

dict_list = data_reader.rows()
print()
print(len(dict_list))
```

Expected output:

```
dict_keys(['field', 'threshold', 'left', 'right'])

{'as_of_year': '2017', 'respondent_id': '33-0975529', 'agency_name': 'Department of Housing and Urban Development', 'agency_abbr': 'HUD', 'agency_code': '7', 'loan_type_name': 'VA-guaranteed', 'loan_type': '3', 'property_type_name': 'One-to-four family dwelling (other than manufactured housing)', 'property_type': '1', 'loan_purpose_name': 'Refinancing', 'loan_purpose': '3', 'owner_occupancy_name': 'Owner-occupied as a principal dwelling', 'owner_occupancy': '1', 'loan_amount_000s': '165', 'preapproval_name': 'Not applicable', 'preapproval': '3', 'action_taken_name': 'Loan originated', 'action_taken': '1', 'state_name': 'Wisconsin', 'state_abbr': 'WI', 'state_code': '55', 'county_name': 'Outagamie County', 'county_code': '87.0', 'applicant_ethnicity_name': 'Not Hispanic or Latino', 'applicant_ethnicity': '2', 'co_applicant_ethnicity_name': 'Not Hispanic or Latino', 'co_applicant_ethnicity': '2', 'applicant_race_name_1': 'White', 'applicant_race_1': '5', 'applicant_race_name_2': '', 'applicant_race_2': '', 'applicant_race_name_3': '', 'applicant_race_3': '', 'co_applicant_race_name_1': 'White', 'co_applicant_race_1': '5', 'co_applicant_race_name_2': '', 'co_applicant_race_2': '', 'applicant_sex_name': 'Male', 'applicant_sex': '1', 'co_applicant_sex_name': 'Female', 'co_applicant_sex': '2', 'applicant_income_000s': '57', 'purchaser_type_name': 'Life insurance company, credit union, mortgage bank, or finance company', 'purchaser_type': '7', 'denial_reason_name_1': '', 'denial_reason_1': '', 'denial_reason_name_2': '', 'denial_reason_2': '', 'population': '5765.0', 'minority_population': '24', 'hud_median_family_income': '74700'}

60
```

### `Loan` Class

The Loan class will provide a convenient way to represent information
about loans.  It will have the following methods:

```python
class Loan:
    def __init__(self, amount, purpose, race, income, decision):
        pass # TODO

    def __repr__(self):
        pass # TODO

    def __getitem__(self, lookup):
        pass # TODO
```

It can be instantiated like this:

```python
loan = Loan(40, "Home improvement", "Asian", 120, "approve")
```

`repr(loan)` should return something like this:

```python
"Loan(40, 'Home improvement', 'Asian', 120, 'approve')"
```

In this example, if you implement `__getitem__` properly, `loan["amount"]` should give 40, `loan["purpose"]`
should give `"Home improvement"`, and so on.

`loan[????]` should work for ANY value in the brackets.  If the value
in the brackets does NOT match one of the parameter names in the
constructor, the behavior will be different.  It will return 0 or 1,
depending on whether any argument passed to those parameters matches
the value in brackets.  For example, `loan["Refinance"]` will be 0,
and `loan["Asian"]` will be 1.

### `Bank` Class

The `Bank` class ties together `ZippedCSVReader` and `Loan`.
Instances can be instantiated like this:

```python
b = Bank(name, reader)
```

, where `name` is a string and `reader` is an instance of your `ZippedCSVReader` class.  A
`loans` method can be used like this:

```python
b = Bank("NCUA", data_reader)
for loan in b.loans():
    print(loan) # loan is of type Loan
```

Expected output:

```
Loan(94, 'Refinancing', 'Information not provided by applicant in mail, Internet, or telephone application', 71, 'deny')
Loan(55, 'Home purchase', 'White', 41, 'deny')
Loan(20, 'Refinancing', 'Black or African American', 41, 'approve')
Loan(22, 'Refinancing', 'White', 36, 'approve')
Loan(175, 'Refinancing', 'White', 70, 'approve')
Loan(191, 'Home purchase', 'Information not provided by applicant in mail, Internet, or telephone application', 68, 'approve')
Loan(82, 'Refinancing', 'White', 40, 'deny')
```

`Bank` is doing two things here: (1) converting dict rows to Loan
objects, and (2) filtering to rows where `agency_abbr` is "NCUA".  As
in `ZippedCSVReader.rows` (which `Bank` uses), `loans` should return
the list of loan objects.  If `None` is passed for the bank name,
`loans()` should return `Loan` objects for all rows in the zip file.

Relevant fields when reading from the CSV: `agency_abbr`,
`applicant_race_name_1`, `loan_amount_000s`, `loan_purpose_name`,
`applicant_income_000s`, `action_taken`.  When converting, `amount`
and `income` should be converted to ints.  Missing values (`""`)
should be replaced with 0.  `action_taken` is 1 for "approve", otherwise `decision` is "deny"

To figure out what bank names (like "HUD") are in the dataset, you
should have a function (not a method!) in `trees.py` that works like
this:

```python
reader = ZippedCSVReader('loans.zip')
names = get_bank_names(reader) # should be sorted alphabetically
print(names)
```

Expected output:

```
['CFPB', 'FDIC', 'FRS', 'HUD', 'NCUA', 'OCC']
```

### `SimplePredictor` Class

Instances of `SimplePredictor` can be used to decide whether to
approve a loan.  You can start from the following:

```python
class SimplePredictor():
    def __init__(self):
        pass

    def predict(self, loan):
        pass

    def get_approved(self):
        pass

    def get_denied(self):
        pass
```

Assuming `spred` is a `SimplePredictor` object, `spred.predict(loan)`
will return True if the loan should be accepted, and False otherwise.
`spred.get_approved()` will return how many applicants have been
approved so far

The policy of SimplePredictor is simple: approve all loans where the
purpose is "Refinancing" and deny all others.

For example, `SimplePredictor` object can be used like this:

```
spred = SimplePredictor()
my_loans = [Loan(175, 'Refinancing', 'White', 70, 'approve'),
            Loan(145, 'Home purchase', 'White', 37, 'deny'),
            Loan(200, 'Home purchase', 'White', 95, 'approve'),
            Loan(414, 'Home purchase', 'White', 300, 'approve'),
            Loan(22, 'Refinancing', 'White', 36, '1')]

for loan in my_loans:
    print(loan, 'predict:', spred.predict(loan))
    print('approved:', spred.get_approved(), 'denied', spred.get_denied())
```

Expected output:

```
Loan(175, 'Refinancing', 'White', 70, 'approve') predict: True
approved: 1 denied 0
Loan(145, 'Home purchase', 'White', 37, 'deny') predict: False
approved: 1 denied 1
Loan(200, 'Home purchase', 'White', 95, 'approve') predict: False
approved: 1 denied 2
Loan(414, 'Home purchase', 'White', 300, 'approve') predict: False
approved: 1 denied 3
Loan(22, 'Refinancing', 'White', 36, '1') predict: True
approved: 2 denied 3
```



### `DTree` Class

Decision Trees are trees that can be used to make predictions (or
decisions).  Consider the following picture:

![simple.json](tree.png)

How can we read the above tree?

Let's say somebody is applying for a 190 (thousand dollar) loan
(`amount=190`) and makes 45 (thousands dollars) per year
(`income=45`).  We see that `"field": "amount"` and `"threshold":
200"`. Since `amount <= 200`, we take the left branch. Next, we see
`"field": "income"` and `"threshold: 35"` from the left child
node. Since `income > 35` we take the right branch. In the right child
node, we see `"field": "class"` and `"threshold: 1"`, which represents
predicted class is 1.  In these trees, class `1` means "approve" and
class `0` means "deny".  This particular loan application is therefore
approved.

In terms of code, a DT (decision tree) has some similarities to a BST
(binary search tree).  In both cases, branches are recursively taken
to the right and left based on thresholds.  With a BST, we're working
with a single value, so the comparisons at all nodes are against that
one value.  With a DT, we're working with a row of data, and each node
tells us not only the threshold, but which field of the row should be
considered.

In class, we often implemented a `Node` class.  Here, for simplicity,
we'll use dictionaries instead of custom objects.  The advantage is
that our trees can then be directly loaded from JSON files, with
minimal processing.

You will, however, implement a `DTree` class to help make predictions
based on the tree of dictionaries.  Complete the following to get
started (`DTree` should inherit from `SimplePredictor`):

```python
class DTree(????):
    def __init__(self, nodes):
        ???? # TODO: call parent constructor

        # a dict with keys: field, threshold, left, right
        # left and right, if set, refer to similar dicts
        self.root = nodes

    def dump(self, node=None, indent=0):
        if node == None:
            node = self.root

        if node["field"] == "class":
            line = "class=" + str(node["threshold"])
        else:
            line = node["field"] + " <= " + str(node["threshold"])
        print("  "*indent + line)
        if ????:
            self.dump(node["left"], indent+1)
        if node["right"]:
            ????
```

Test your code.  You should be able to create a DTree based on nested
dicts, then dump it, as follows:

```python
node_dicts = {
    "field": "amount",
    "threshold": 200,
    "left": 
        {
        "field": "income",
        "threshold": 35,
        "left": 
            {
            "field": "class",
            "threshold": 0,
            "left": None,
            "right": None
            },
        "right": 
            {
            "field": "class",
            "threshold": 1,
            "left": None,
            "right": None
            }
    },
    "right": 
        {
        "field": "income",
        "threshold": 70,
        "left": 
            {
            "field": "class",
            "threshold": 0,
            "left": None,
            "right": None
            },
        "right": 
            {
            "field": "class",
            "threshold": 1,
            "left": None,
            "right": None
        }
    }
}

dt = DTree(node_dicts)
dt.dump()
```

You should see something like this (note that this simple text representation is equivalent to the earlier tree diagram):

```
amount <= 200
  income <= 35
    class=0
    class=1
  income <= 70
    class=0
    class=1
```

Of course, you won't usually paste large tree dicts into your code.
It makes more sense to use your `load_json` method from earlier to
read a dict tree from a JSON inside a zip file.  The following
achieves the same result as above:

```python
tree_reader = ZippedCSVReader("trees.zip")
dt = DTree(tree_reader.load_json("simple.json"))
dt.dump()
```

**Dictionary Format**: each dictionary contains four fields: `field`
(type of the value ie. amount, income, etc.), `threshold` (the value
held in the dictionary), `left` (<= current value), and `right` (>
current value).  Dictionaries with a field of "class" treat the fields
a little differently.  They are guaranteed to be leaf nodes (`left`
and `right` will be None) and `threshold` is interpreted as the
prediction value of 0 or 1 (instead of a value for comparison as in
non-leaf nodes).

For now, add one more recursive method named `node_count` to `DTree`
that counts the number of nodes in the tree.  The following should
return 61, for example:

```python
tree_reader = ZippedCSVReader("trees.zip")
dt = DTree(tree_reader.load_json("good.json"))
dt.node_count()
```

# Individual Part (25%)

You have to do the remainder of this project on your own.  Do not
discuss with anybody except 320 staff (mentors, TAs, instructor).

### `DTree.predict` Method

Add a recursive `predict` method that takes a Loan object and
traverses the nodes of the decision tree to determine whether or not
to approve the loan.  `predict` should return True or False, and
should work like this:

```python
tree_reader = ZippedCSVReader("trees.zip")
dt = DTree(tree_reader.load_json("simple.json"))
loan = Loan(40, "Home improvement", "Asian", 120, "approve")
dt.predict(loan)
```

The above returns True, but to manually test your code (before running
the tester.py), try changing the `amount` and `income` values to
trigger decisions based on each of the leaf nodes in the decision
tree.

### Bias Testing

Here's one possible way to measure racial bias in a predictor: for a
given set of loan applications, how often would the outcome
(approve/deny) have been different if the applicant was of a different
race, but was otherwise identical on all stats?

Complete the following function to answer this question:

```python
def bias_test(bank, predictor, race_override):
    pass
```

1. use bank to iterate over loans with `loans`
2. for each loan, feed it directly to predictor, and store the result
3. modify the loan, changing the race of applicant to `race_override`
4. feed the modified loan to the predictor again, and compare new result to previous result
5. at the end, return the percentage of cases where the predictor gave a different result after the race was changed

Here's an example:

```python
b = Bank(None, ZippedCSVReader("loans.zip"))
dt = DTree(ZippedCSVReader("trees.zip").load_json("bad.json"))
bias_percent = bias_test(b, dt, "Black or African American")
print(bias_percent)
```

Here, the result should be `0.4112`.  The decision tree in "bad.json"
is exhibiting major bias with respect to Black and African American
applicants, with race being a deciding factor 41% of the time.

## Conclusion

When we build models to mimic human behavior, we need to be careful
that our models don't also become biased.  In this project, we tested
a number of models for one kind of bias (racial).  The HDMA data set
is quite extensive.  Take a moment to think about what other biases
you might want to check for before using decision trees (or other
models) to make loan decisions for real people.  For inspiration, here
are some of the columns in the HDMA dataset:

```
as_of_year, respondent_id, agency_name, agency_abbr, agency_code,
loan_type_name, loan_type, property_type_name, property_type,
loan_purpose_name, loan_purpose, owner_occupancy_name,
owner_occupancy, loan_amount_000s, preapproval_name, preapproval,
action_taken_name, action_taken, state_name, state_abbr, state_code,
county_name, county_code, applicant_ethnicity_name,
applicant_ethnicity, co_applicant_ethnicity_name,
co_applicant_ethnicity, applicant_race_name_1, applicant_race_1,
applicant_race_name_2, applicant_race_2, applicant_race_name_3,
applicant_race_3, co_applicant_race_name_1, co_applicant_race_1,
co_applicant_race_name_2, co_applicant_race_2, applicant_sex_name,
applicant_sex, co_applicant_sex_name, co_applicant_sex,
applicant_income_000s, purchaser_type_name, purchaser_type,
denial_reason_name_1, denial_reason_1, denial_reason_name_2,
denial_reason_2, population, minority_population,
hud_median_family_income
```
