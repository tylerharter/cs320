# IN PROGRESS!!!!

# DON'T START YET!!!!!

# P6: Hospital Readmission

When patients are admitted to a hospital, the type of care they
receive may affect whether they'll be readmitted again in the near
future.  In this project, we'll look at data about length of stay and
readmissions for patients with diabetes.

You'll be answering questions (using the `#qN` format) in a .ipynb
notebook file, much like you did for P1.  You'll be primarily using
sklearn to learn about the data.  The main challenge will be getting
the data into a form that can readily used as sklearn input.

## Corrections/Clarifications
* none yet

## Dataset

Take a quick look at the following paper:

Beata Strack, Jonathan P. DeShazo, Chris Gennings, Juan L. Olmo,
Sebastian Ventura, Krzysztof J. Cios, and John N. Clore, "<a
href="http://downloads.hindawi.com/journals/bmri/2014/781670.pdf">Impact
of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000
Clinical Database Patient Records</a>," BioMed Research International,
vol. 2014, Article ID 781670, 11 pages, 2014.

Pay close attention to criteria the researchers used to build this
dataset (start of section 2.2 on page 2) and the description of
various fields (Table 1 on page 3).

The data described can be found here:
https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008.
We've included the `dataset_diabetes.zip` file for you to use here on
GitHub.

The most important data is in the `diabetic_data.csv` file inside this
zip.  Load that a DataFrame and get familiar with the columns.  Note
that missing data is represented by question marks ("?") --
unfortunately, not all hospitals collected the same information about
visits.

## Part 1: Train/Test Split

In machine learning, it is easy to accidentally train models that
simply memorize details of the data rather than capturing meaningful
patterns -- this is called overfitting.

To check whether this is happening, models are usually trained on a
training set, then evaluated on both the training set and a separate
test set.  A model that does much worse on test data than training
data likely overfitted.

You should split the rows of the original DataFrame (from
`diabetic_data.csv`) into DataFrames named `train` and `test`.

Training+test datasets are often formed by randomly splitting the
original data in some way.  To simply our auto-grading, you will
instead split based on the following rule:

Add up all the digits in the `encounter_id` and `patient_nbr` columns
together.  If the sum is even for a row, that row should go to
`train`; else, it should go to `test`.

For example, the first row has encounter_id 2278392 and patient_nbr
8222157.  This is a training row as (2+2+7+8+3+9+2) + (8+2+2+2+1+5+7)
= 60, an even number.



#### Q1: What are the shapes of the `train` and `test`?

After you've built the DataFrames, just paste this in a cell to answer this question:

```python
#q1
train.shape, test.shape
```

#### Q2: Is `time_in_hospital` similar between test and training?

Answer with a tuple giving the means and standard devations for this
field in both datasets, like this:

```python
#q2
(
    train["time_in_hospital"].mean(),
    test["time_in_hospital"].mean(),
    train["time_in_hospital"].std(), 
    test["time_in_hospital"].std(),
)
```

We're doing this to sanity check that our scheme for splitting the
into the two datasets into test/training (checking the oddness of the
sum of digits) isn't producing very disimilar subsets.

#### Q3: Is `readmitted` similar between test and training?

Answer with a nested dict, like this:

```python
#q3
{
    "train": dict(train["readmitted"].value_counts()),
    "test": dict(test["readmitted"].value_counts()),
}
```

#### Q4: How much data is missing in each column?

Answer with a dictionary, where each key is the name of a column
containing at least some missing data, and the value is the percent
(out of 100) of data that is "?".  Don't include columns with no
missing data in the dictionary.

## Part 2: Heat Maps

## Part 3: Regressions

## Part 4: PyTorch Practice

## Part 5: Logistic Regression

## Part 6: Clustering
