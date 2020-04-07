# DRAFT ONLY

# DON'T START, NOT READY YET!!!!

# Final Exam

The final "exam" is really an open-ended analysis project.  Hopefully
it's fun to be free of the usual constraints!  You'll be building a
static website (no flask) to share your analysis on a topic of your
choosing.  You'll write Python code (in .ipynb or .py files -- your
choice) to generate plots as image files to use in the site.

Being a good data scientist requires you to be a both a detective and
a teacher.  You need to discover truths about your topic, then
effectively share them with your audience.

**Detective:** You will only include 10 visualizations on your site,
but your project won't be very good if you only create 10 plots in the
process.  You should generate dozens of plots for yourself and invest
serious time reflecting on them so that you can learn something about
your chosen topic.

**Teacher:** After your can articulate the most import insights,
carefully decide what 10 visualizations best reveal the lessons you
learned.  It's OK (and good) if most of your visualizations get pruned
out of the final product.  The 10 visualizations in their final form
should be highly refined, hopefully not like anything you created when
doing your detective work.

The writing that accompanies your plots will be of upmost importance.
Read this essay by venture capitalist Paul Graham on useful writing
before you get started: http://www.paulgraham.com/useful.html.

## Deadlines

* Apr 20 (Mon): proposals are due (submit at https://forms.gle/v1fjnoLMPVr8Yie26)
* Apr 24 (Fri): send one plot+text to peers for feedback
* Apr 27 (Mon): peer feedback due back
* May 3 (Sun): final.zip is due

If you miss the proposal deadline, you will be required to work
individually (instead of with a team) for the final.

final.zip will not be accepted late (because we'll be in a time crunch
to get final grades out since we can't automatically grade this one).
So please submit whatever you have on May 3, even if incomplete.

## Submission

Hand in a `final.zip` file as P7 that contains your code, pages, and
graphics.  If the data is small, include that too.

We should be able to perform the following steps to evaluate your
work:

1. `unzip final.zip`
2. `cd final`
3. `python3 -m http.server --bind 127.0.0.1 8000`
4. open `http://127.0.0.1:8000/index.html` in a web browser

## Collaboration

We recommend forming teams of 2 for the final project.  If you like,
you may also form a team with as many as 4 people.  Though it's
discouraged, you may also choose to work alone.

Consider posting to piazza under the "final-discussion" folder about
possible topics to find potential collaborators who share your
interests.

You may receive help from students on other teams, as long as (a) they
did not choose a very similar topic for their project, and (b) you
cite the help you received.

After you submit your proposal, we'll pair you with another team for
peer feedback on some initial results (one visualization accompanied
by some text).

For other CS 320 projects, you are never allowed to post your work
publicly online, even after the semester ends.  For this final "exam",
you are allowed to publish your work after the semester ends, but
please don't do so before final grades are released. We don't want
teams working on similar projects to copy your code.

## Proposal

Submit it here by Monday, April 20th: https://forms.gle/3DfVmQeHGdPH4yfUA

Let us know the topic, and who will be collaborating on it.  Only one
team member should submit.

Provides URLs to the data you'll use.  You should rely on at least two
different data files.  Kaggle is not allowed as a source (others have
usually done the hard preprocessing work for those datasets).

Describe the audience for whom you're doing the analysis.  You should
assume your audience is technical (for example, they've taken CS 320),
so this is more about what other background they have.

List some of the questions you want to answer and potential
actions/policies that will be evaluated.  Be sure to tie this to the
audience.  For example, if the audience is local elected officials, it
would not be appropriate to evaluate country-wide federal policies.

## Pages

You should have the following pages:

* index.html
* data.html
* results.html (most important)
* acks.html

The home page should include title, names, wiscmail addresses, one
paragraph summary of the project, and links to the other pages.  Other
pages are described below.

## Page: data.html

Describe the data files you're using and the columns in any tables.
You may quote other documentation if you like (put in quotes and
include a link), but it's your responsibility to make sure this
documentation isn't ambiguous, so either (a) avoid using any data
fields you don't understand or (b) dig deeper until you can write
better documentation than what's in the original.

If the data is too large to include in final.zip, include directions
(code snippets, bash commands, etc) on how to grab the data.

## Page: results.html

This page should have visuals interleaved with text.

### Visuals

Your results.html page should have exactly 10 visualizations (mostly
plots, but also maps and animations).  These 10 should include at least
one of each of the following:

1. stacked bar plot
2. clustered bar plot
3. line plot with multiple lines
4. scatter plot with regression line showing a correlation between two variables
5. scatter plot with multiple markers representing different categories
6. a plot with multiple subplots
7. geographic map
8. animation

Notice that you have 2 plots remaining where you can pick the style
yourself -- or perhaps more, if you satisfy multiple requirements with
the same plot (for example, you could satisfy the last two with a
single animated map).

An important grading criterion is that you identify cases where each
of the above is the best form of plot.  For example, using a clustered
bar plot where a stacked one would be more appropriate would not
receive a good score.  Consider reviewing this:
https://tyler.caraza-harter.com/cs301/fall19/readings/axes.html#Picking-the-Right-Plot.

Here's an example of a horrible animated bar plot:
https://www.reddit.com/r/dataisbeautiful/comments/fumbza/oc_coronavirus_covid19_daily_cases_by_country_per/.
A simple plot with time on the x-axis and one line per country
would have saved time and made the trends more apparent.  Being
informative matters, being flashy doesn't.  You're more than welcome
to make all visuals gray scale, if you like.

If you use visualization tools beyond what we learned in class, they
shouldn't depend on any online resources each time they're displayed
(I'm specifically thinking of folium, which I dislike because it
re-fetches map data evertime a map is shown, but this applies to any
tool that behaves this way).

### Text

Each plot should be preceded by an explicit question and followed by
observations and conclusions.

Most of the observations should be quantitative.  Instead of "we
observe category B is biggest", say "we observe that the largest
category, B, accounts for 73% of the total".  Instead of "the number
of occurrences rises steeply over time", say "the number of
occurrences increases by about 210 per year" (perhaps based on the
slope of a regression you did in the plot).

An interesting conclusion goes beyond observation, perhaps talking
about implications, policies, and followup questions.  If you ask a
followup question, then actually followup in the next plot if you can
(don't leave the reader hanging!).  Use the text to connect one plot
to the next, or to give a preview of why different plots will go in
different sections.

## Page: acks.html

This acknowledgments page should list any people or online resources
you used to complete your project.

There's no specific format required, but be comprehensive.

You don't need to cite help from your instructor or TAs.

We'll be doing a round of peer feedback on a single plot and some
accompanying text.  Plots will be sent by Apr 24 and feedback by Apr
27.  The ack page should contain a before/after version of this
content, along with the peer feedback (so we can see how you
integrated the suggestions).

## Grading

The Python code for generating all the plots must be included in the
.zip, or the submission will not be accepted.  The grading breakdown
is as follows:

* 5% proposal
* 5% - home page
* 10% - data page
* 10% - acknowledgments page, giving peer feedback, integrating feedback received
* 70% - results page

Of that 70%, 10% is for overall writing.  Does some short intro text
set up the problem well?  Does the conclusion use the results to
support actionable suggestions for the audience (as identified in the
proposal)?  How natural is the organization (sequence and/or
hierarchy) of the material?  In terms of sequence, it's nice when the
conclusions of one plot raise a question that motivates the following
plot.  In terms of hierarchy, you could potentially show a first plot
that shows important categories of the problem, then have sections
(with `<h2>` tags) addressing each category.

Each plot and it's accompanying text is worth 6% of the total.  We'll
deduct if there are more or less than 10 plots.

Here are examples of things that might result in deductions on a plot and its text:
* lack of axis labels or lack on units
* tick labels with too many zeros (instead of having a label 20000000, it should be 20, with "millions" in the label)
* text too small
* unclear what different marks mean
* unclear what is being measured
* not ideal plot style for what is being shown
* unhelpful redundancy
* missed opportunities to breakdown the data into finer categories to better expose the patterns
* plot gives emphasis to something other than what you're trying to show (as determined by your conclusions)
* lack of an explicit question before the plot (or a boring question)
* lack of observations/conclusions following the plot
* conclusions that are not supported (or worse, contradict) the plot
* conclusions that are qualitative when it would be easy to make them quantitative (quantitative is better)
* results that seem too unrealistic, and aren't supported with text and additional plots convincing the reader that there's a very surprising result (as opposed to a bug in the analysis code)
* accompanying text with severe grammatical or spelling errors
* excessive verbosity
* other...

## Conclusion

Overall, have fun with this one!  Although there are lots of details,
keep in mind that your big goal is to present your analysis in a way
so that whoever is grading you (or reading your site) learns something
interesting in the process.

If you accomplish that big goal, we'll avoid being too nitpicky about
the deductions.  Learning entails remembering -- what do you really
hope somebody who reads your site will remember a month later and will
want to tell their friends?  Make sure you know what those lessons
are, then leverage all your text and visuals to make them stand out!
