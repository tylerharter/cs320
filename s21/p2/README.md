# Project 2: Decision Trees and Bias

## Overview

In this project, you'll learn about zip files, modules, object
oriented programming, and trees.

You will implement all classes and functions in tree.py file for this project.This is where all of your code will go.  For your own testing and debugging,we recommend creating a notebook where you do `import tree` and use the functions and classes in your module.

You will end up implementing the following classes.

```
class ZippedCSVReader
class Loan
class Bank
class SimplePredictor
class DTree
```

For testing, you'll need to download the .zip files, tester.py, and
expected.json. tester.py will test whether each class and class methods are properly implemented.

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

We're providing `loans.zip`, `mini.zip`.  This class
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

For this, you can refer to lab3 part2 (https://github.com/tylerharter/cs320/blob/master/s21/lab3/part2.md).



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
all .csv files in alphabetical order). `lines` and `csv_iter` should return the list of rows in files

```python
def lines(self, name):
    rows = []
    with ZipFile(self.filename) as zf:
        with zf.open(name) as f:
            for line in TextIOWrapper(f):
                rows.append(line)
    return rows
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
As in `csv_iter` (which `Bank` uses), `loan_iter` should return the list of loan objects.

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

`loan_min` and `loan_max` are both inclusive, which means you will filter data with the condition `loan_min <= x <= loan_max`.



# Individual Part (25%)

You have to do the remainder of this project on your own.  Do not
discuss with anybody except 320 staff (mentors, TAs, instructor).

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

* `dtree.readTree(path)` will take a file path (such as `os.path.join(trees,simple.json)`) that will be read from a json file and build a decision tree using its contents (a bit more on this below). It is not required to return anything. To read json file, you can review lab3 part1 (https://github.com/tylerharter/cs320/blob/master/s21/lab3/part1.md).
* `dtree.predict(data)` will return True for loan approved and False for loan disapproved using the tree built in `readTree`
* `dtree.getDisapproved()` will return how many applicants have been disapproved so far

The following code snippet should create a tree and make one prediction:

```python
dtree = tree.DTree()
file_path = os.path.join('trees', 'simple.json')
dtree.readTree(file_path)
dtree.predict(loan)
```

Having a separate `Node` class will almost certainly be helpful, but
we don't require it.

#### simple.json

While there are other json files like this one, we will just go through
this one as a bit of an example.

```
{
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
            "left": null,
            "right": null
            },
        "right": 
            {
            "field": "class",
            "threshold": 1,
            "left": null,
            "right": null
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
            "left": null,
            "right": null
            },
        "right": 
            {
            "field": "class",
            "threshold": 1,
            "left": null,
            "right": null
        }
    }
}
```

The decision trees can be read in as a series of nested dictionaries. Each 
dictionary contains four fields: field (type of the value ie. amount, income, etc.), 
threshold (the value held in the dictionary),left (<= current value), and right (> current value). 
The dictionary itself can be thought of as the tree, with the inner dictionaries being the nodes 
as you traverse down the tree. Dictionaries with a field of 'class' can be thought of as the leaf nodes. 'threshold' in Dictionaries with a field of 'class' can be interpreted as the prediction value, which is 0 or 1.

How can we read the above tree?

Let's say somebody is applying for a 190 (thousand dollar) loan (`amount=190`) and
makes 45 (thousands dollars) per year (`income=45`).  We see that `"field": "amount"` and `"threshold": 200"`. Since `amount <= 200`, we take the left branch. Next, we see `"field": "income"` and `"threshold: 35"` from the left child node. Since `income > 35` we take the right branch. In the right child node, we see  `"field": "class"` and `"threshold: 1"`, which represents predicted class is 1.  In these trees, class
`1` means "approve" and class `0` means "deny".  This particular loan
application is therefore approved.

#### Hints:

* This is a binary tree!

* When `json.load` is used, you will be able to get nested dictionaries. From nested dictionaries, you should parse it to make Node and DTree instances.

* The binary tree for simple.json can be visualized as follows.

  ```
  ![simple.json](simple.json)
  ```

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

dtree = tree.DTree()
dtree.readTree(tree_reader, os.path.join("trees", "bad.json")
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
