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

Answer the following questions with respect to the training data (not
the original dataset!).

#### Q5: How common is each pairing of `admission_source_id` to `discharge_disposition_id`?

Output should be a DataFrame, like the "Question 5" one in
`expected.html`.  The index contains every unique
`admission_source_id` and the columns correspond to every unique
`discharge_disposition_id`.  Each cell is an integer, representing how
many rows have each admission/discharge combo.

The order of the rows/columns in the output is not important to the
tester.

To satisfy the tester, you will need to tweak the display options so
data is not hidden by ellipses (`...`):

https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html

You may want to reset the display option after the question.

#### Q6: How common is each pairing of admission source to discharge disposition?

This is the same as last time, but now codes are replaced with
descriptions, like in the "Question 6" table in `expected.html`.

This question is actually very challenging because the
`dataset_diabetes/IDs_mapping.csv` file is weirdly formatted.  We
didn't make it so -- this is an example of real-world messiness you'll
often encounter as a data scientist.  Basically, there are three CSVs
jammed together into one .csv file.  Each of the three is separated by
a line that is empty, except for one comma.

Once you pull the data out of `IDs_mapping.csv`, you may want to use
the following function to add real index/column names to your
DataFrame from `#q5`, without recomputing everything from scratch:

https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html

#### Q7: How common is each pairing of admission source to discharge disposition? [Heat Map]

This is the same as the last one, but now, instead of producing a table, you should produce a heatmap, like this:

<img width=800 src="heatmap.png">

Hints:

* here's an example of how to create a square heatmap from a DataFrame (not that your DataFrame is NOT square): https://www.pythonprogramming.in/generate-a-heatmap-in-matplotlib-using-pandas-data.html
* we used the `cmap="binary"` to make darker values correspond to larger numbers
* a few combinations dominate -- to make the others visible, take the `log2` of each number before calling `plt.imshow`.  As `log2(0)` is not defined, add 1 to each cell before taking the `log2`.  Why is it valid for us to make these seemingly arbitrary transformations?  Because color is inherently subjective (unlike, say, distance along an axis), so we only care about the relative, namely that darker=more.

## Part 3: Regressions

Add a column to your train and test datasets named `visits` that sums
the three kinds of visits already in the data: 

length of stay vs. total visits
length of stay vs. visits
length of stay vs. demographics

## Part 4: PyTorch Practice

animated regression finder

## Part 5: Logistic Regression

readmission vs. length of stay (non-polynomial?)
readmission vs. drugs (one hot, PCA?)
missing data vs. demographic

## Part 6: Clustering

visit types