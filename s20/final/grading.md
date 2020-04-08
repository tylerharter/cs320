# Grading

The Python code for generating all the plots must be included in the
.zip, or the submission will not be accepted.  The grading breakdown
is as follows:

* [5%] proposal
* [5%] home page
* [10%] data page
* [10%] acknowledgments page, giving peer feedback, integrating feedback received
* [60%] visualizations and accompanying text on results page (6% per each of 10 plots)
* [10%] general writing on results page

## Visualizations

We'll deduct points if there are more or less than 10 visualizations,
or if any of the six required plot styles are missing.

Here is a **non-exhaustive** list of things that might result in deductions on a plot:

* lack of axis labels or lack of units
* tick labels with too many zeros (instead of having a label 20000000, it should be 20, with "millions" in the label)
* text too small
* unclear what different marks mean
* unclear what is being measured
* not ideal plot style for what is being shown
* unhelpful redundancy
* missed opportunities to breakdown the data into finer categories to better expose the patterns.  For example, it's usually possible to upgrade a simple bar plot into a stacked bar plot by breaking each bar into categories, exposing the composition of a total.

Or the related text...

* lack of an explicit question before the plot (or a boring question)
* lack of observations/conclusions following the plot
* conclusions that are not supported by the plot, or worse, contradict it
* conclusions that are qualitative when it would be easy to make them quantitative (quantitative is better)
* plot gives emphasis to something other than what you're trying to show (as determined by your conclusions)
* results that seem too unrealistic, and aren't supported with text and additional plots convincing the reader that there's actually a very surprising result (as opposed to a bug in the analysis code or error in the original data)
* accompanying text with severe grammatical or spelling errors
* unclear writing or excessive verbosity

These are high standards.  Most plots are likely to receive some
deduction.  A deduction on a plot doesn't mean you did bad work, it
means there is room to further improve.

## General Writing

Does some short intro text set up the problem well?  Does the
conclusion use the results to support actionable suggestions for the
audience (as identified in the proposal)?  How natural is the
organization (sequence and/or hierarchy) of the material?

In terms of sequence, it's nice when the conclusions of one plot raise
a question that motivates the following plot.  In terms of hierarchy,
you could potentially show a first plot that shows important
categories of the problem, then have sections (with `<h2>` tags)
addressing each category.