# Project 2: Decision Trees and Bias

## Corrections/Clarifications

* Oct 2: fixed testDTree:predict in tester.py 
* Sep 30: fix `readTree` documentation
* Sep 30: rename `data_reader` to `reader` to clarify example
* Sep 30: show results of how our classifier behaves on each loan for testBiasLargeFile in the debug directory

## Overview

In this project, you'll learn about zip files, modules, object
oriented programming, and trees.

You will be creating one `tree.py` file for this project. This is
where all of your code will go.  For your own testing and debugging,
we recommend creating a notebook where you do `import tree` and use
the functions and classes in your module.

For testing, you'll need to download the .zip files, tester.py, and
expected.json.

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
sufficient dataset, will they overgeneralize?  In this project, we'll
be providing several files describing decision trees.  Decisions trees
are a kind of model that can output things like approve/deny on a
row-by-row basis.  Your job will be to write Python code to load and
run the decision trees.  At least one of them is racially biased, and
you'll be asked to write a function that exposes this.

# Group Part (75%)

For this portion of the project, you may collaborate with your group
members in any way (even looking at working code).  You may also seek
help from 320 staff (mentors, TAs, instructor).  You <b>may not</b>
seek receive help from other 320 students (outside your group) or
anybody outside the course.

## `ZippedCSVReader` Class

We're providing `loans.zip`, `mini.zip`, and `trees.zip`.  This class
will help your other code access the data.  Here are a couple examples
of how the class is instantiated:

```python
data_reader = ZippedCSVReader("mini.zip")
tree_reader = ZippedCSVReader("trees.zip")
```

After the above call, it should be possible to see a list of files via a `path` attribute, like this:

```python
print(data_reader.paths) # in alphabetical order!
```

Your reader needs to work with large files.  This means it cannot read
all the lines to a list, or to a DataFrame (there may not be enough
memory!).  Instead, you'll write methods that `yield` rows/lines one
at a time.

Your reader will have two methods: `lines` and `csv_iter`.  They can
be used as follows:

```python
# loop over all lines in file.txt
for row in reader.lines("file.txt"):
    pass

# loop over all rows as OrderedDicts from any CSV in the zip
for row in reader.csv_iter():
    pass

# loop over all rows as OrderedDicts from specific.csv in the zip
for row in reader.csv_iter("specific.csv"):
    pass
```

As you can see, both take a file name.  But for `csv_iter`, it is
optional; if not passed, it essentially concatenates all CSV data (use
all .csv files in alphabetical order).

The `lines` method looks like this:

```python
    def lines(self, name):
        with ZipFile(self.filename) as zf:
            with zf.open(name) as f:
                for line in TextIOWrapper(f):
                    yield line
```

For `csv_iter`, you'll want to do something similar, but you'll need
to figure out how to use `csv.DictReader` to pull in each CSV row as
an OrderedDict:
https://docs.python.org/3/library/csv.html#csv.DictReader.

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
loan = tree.Loan(40, "Home improvement", "Asian", 120, "approve")
```

In this example, `loan["amount"]` should give 40, `loan["purpose"]`
should give `"Home improvement"`, and so on.

`loan[????]` should work for ANY value in the brackets.  If the value
in the brackets does NOT match one of the parameter names in the
constructor, the behavior will be different.  It will return 0 or 1,
depending on whether any argument passed to those parameters matches
the value in brackets.  For example, `loan["Refinance"]` will be 0,
and `loan["Asian"]` will be 1.

`repr(loan)` should return something like this:

```python
"Loan(40, 'Home improvement', 'Asian', 120, 'approve')"
```

### `Bank` Class

The `Bank` class ties together `ZippedCSVReader` and `Loan`.
Instances can be instantiated like this:

```python
b = Bank(name, reader)
```

`reader` is an instance of your `ZippedCSVReader` class.  A
`loan_iter` object can be used like this:

```python
reader = ZippedCSVReader('loans.zip')
b = Bank("HUD", reader)
for loan in b.loan_iter():
    pass # loan is of type Loan
```

`Bank` is doing two things here: (1) converting OrderedDicts rows to
Loan objects, and (2) filtering to rows where `agency_abbr` is "HUD".
As in `csv_iter` (which `Bank` uses), `loan_iter` should use `yield`.

When converting, `amount` and `income` should be converted to ints.
Missing values (`""`) should be replaced with 0.

To figure out what bank names (like "HUD") are in the dataset, you
should have a function (not a method!) in `trees.py` that works like
this:

```python
names = get_bank_names(reader) # should be sorted alphabetically
```

Finally, `Bank` should have a method like `loan_iter` that does additional filtering:

```python
def loan_filter(self, loan_min, loan_max, loan_purpose):
```

`loan_min` and `loan_max` are inclusive.

### `SimplePredictor` Class

Instances of `SimplePredictor` can be used to decide whether to
approve a loan.  You can start from the following:

```python
class SimplePredictor():
    def predict(self, loan):
        pass

    def getApproved(self):
        pass
```

Assuming `spred` is a `SimplePredictor` object, `spred.predict(loan)`
will return True if the loan should be accepted, and False otherwise.
`spred.getApproved()` will return how many applicants have been
approved so far

The policy of SimplePredictor is simple: approve all loans where the
purpose is "Home improvement" and deny all others.

### `DTree` Class

The `DTree` class (which stands for Decision Tree) will provide you
with a better means of predicting whether or not an applicant should
have their loan accepted.  Your `DTree` class must inherit from
`SimplePredictor`. (While it is simple, there's some stuff in there we
can still use!) There are several methods should `DTree` class should
have.  Assuming `dtree` (creative name, I know) is an object of your
`DTree` class:

* `dtree.readTree(reader, path)` will take a file name (such as `simple.txt`) that will be read from a zip via the reader (of type ZippedCSVReader) and build a decision tree using its contents (a bit more on this below). It is not required to return anything
* `dtree.predict(data)` will return True for loan approved and False for loan disapproved using the tree built in `readTree`
* `dtree.getDisapproved()` will return how many applicants have been disapproved so far

The following code snippet should create a tree and make one prediction:
```python
tree_reader = tree.ZippedCSVReader('trees.zip')
dtree = tree.DTree()
dtree.readTree(tree_reader, "simple.txt")
dtree.predict(loan)
```  
  
Having a separate `Node` class will almost certainly be helpful, but
we don't require it.

#### simple.txt

While there are other txt files like this one, we will just go through
this one as a bit of an example.

```
|--- amount <= 200
|   |--- income <= 35
|   |   |--- class: 0
|   |--- income >  35
|   |   |--- class: 1
|--- amount >  200
|   |--- income <= 70
|   |   |--- class: 0
|   |--- income >  70
|   |   |--- class: 1
```

Let's say somebody is applying for a 190 (thousand dollar) loan and
makes 45 (thousands dollars) per year.  We see that `amount <= 200` is
True (and `amount > 200` is not), so we take the first branch.  Next,
we see `income <= 35` is False, but `income > 35` is True, so we take
the second branch.  Finally, we end up at `class: 1`.  In these trees,
`1` means "approve" and `0` means "deny".  This particular loan
application is therefore approved.

#### Hints:

* this is a binary tree!
* in this format, the root node isn't shown, but you still need to add it
* leaves have a "class", and other nodes have a split field and threshold
* consider splitting on "---".  The number of bars on the left tells you the node depth: "|   |" has depth 2 (the node, not show, has depth 0)
* notice that the information is a little redundant.  Instead of storing "amount <= 200" and "amount >  200" in the two children of the root,** it makes more sense to store this information once in the root node** (split key is "amount", threshold is 200). The left child would be considered either <= being true or > true, and the right child would be the other. 
* each line represents a node.  If you loop over them one at a time, how do you find the parent node?  Here's an observation: if you are on a line for a depth-5 node, it's parent is depth-4 node most recently added to the tree.  One strategy is to keep a dictionary where the key is the depth and the value is the node most recently added at that level.
* this can also be done recursively. It would probably be easiest to not call it recursively by line, but to call it for each node (so in the call for root, it would be called twice, once for root.left and once for root.right). 
* the binary tree for simple.txt should be similar to tree.jpg (located in this repo)

  
# Individual Part (25%)

You have to do the remainder of this project on your own.  Do not
discuss with anybody except 320 staff (mentors, TAs, instructor).

### `RandomForest` Class

While decision trees are a fine machine learning algorithm by
themselves, there is a fantastic upgrade to them. That upgrade is to
random forests. As you might guess from the terminology, a random
forest is made up of many decision trees.  The trees learned their
rules by looking at different data.  A random forest takes a vote: do
the majority of trees say approve or deny?

You can start from the following:

```python
class RandomForest(SimplePredictor):
    def __init__(self, trees):
        pass

    def predict(self, loan):
        pass
```

`trees` is a list of `DTree` instances that will vote.  `predict`
takes their vote and returns the majority opinion.  Break ties however
you like (we'll only test with an odd number of trees).

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

1. use bank to iterate over loans with `loan_iter`
2. for each loan, feed it directly to predictor, and store the result
3. modify the loan, changing the race of applicant to `race_override`
4. feed the modified loan to the predictor again, and compare new result to previous result
5. at the end, return the percentage of cases where the predictor gave a different result after the race was changed

Here's an example:

```python
reader = tree.ZippedCSVReader("loans.zip")
b = tree.Bank(None, reader)

tree_reader = tree.ZippedCSVReader("trees.zip")
dtree = tree.DTree()
dtree.readTree(tree_reader, "bad.txt")
bias_percent = tree.bias_test(b, dtree, "Black or African American")
print(bias_percent)
```

Here, the result should be `0.4138`.  The decision tree in "bad.txt"
is exhibiting major bias with respect to Black and African American
applicants, with race being a deciding factor 41% of the time.

## Conclusion

When we build models to mimic human behavior, we need to be careful
that our models don't also become biased.  In this project, we tested
a number of models for one kind of bias (racial).  The HDMA data set
is quite extensive.  Take a moment to think about what other biases
you might want to check for before using decision trees to make loan
decisions for real people.  For inspiration, here are some of the
columns in the HDMA dataset:

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
