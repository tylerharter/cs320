# Final Exam

## Corrections/Clarifications
* May 1, 2020: the submission site doesn't support multiple partners, but you're allowed to have them, so just click "Ignore Errors" when submitting.  We'll make sure everybody gets their grade based on the proposals you submitted.

## Overview

The final "exam" is really an open-ended analysis project.  Hopefully
it's fun to be free of the usual constraints!  You'll be building a
static website (no flask) to share your analysis on a topic of your
choosing.  You'll write Python code (in .ipynb or .py files -- your
choice) to generate plots as image files to use in the site.

Being a good data scientist requires you to be both a detective and
a teacher.  You need to discover truths about your topic, then
effectively share them with your audience.

**Detective:** You will only include 10 visualizations on your site,
but your project won't be very good if you only create 10 plots in the
process.  You should generate dozens of plots for yourself (a loop
might generate many plots with the same code snippet!) and invest
serious time reflecting on them so that you can learn something about
your chosen topic.

**Teacher:** After you can articulate your most important insights,
carefully select 10 visualizations that best communicate the lessons
you learned.  It's OK (and good) if most of your visualizations get
pruned out of the final product.  The 10 visualizations in their final
form should be highly refined, hopefully not like anything you created
when doing your detective work.

The writing that accompanies your plots will be of utmost importance.
Read this essay by venture capitalist Paul Graham on useful writing
before you get started: http://www.paulgraham.com/useful.html.

Other links:
* [page requirements](pages.md)
* [grading standards](grading.md)

## Deadlines

* Apr 20 [Mon] - [proposals](#proposal) due
* Apr 24 [Fri] - send one plot (and corresponding text) to peers for feedback
* Apr 27 [Mon] - peer feedback due back
* May 3 [Sun] - final.zip is due

If you miss the proposal deadline, you will be required to work
individually (instead of with a team) for the final.

final.zip will not be accepted late.  We'll already be in a time
crunch to get final grades out since we can't automatically grade this
one.  So please submit whatever you have on May 3, even if incomplete.

## Collaboration

We recommend forming teams of 2 for the final project.  Teams with as
many as 4 students total (including yourself) are allowed.  Though
it's discouraged, you may also choose to work alone.

Consider posting to piazza under the "final-discussion" folder about
possible topics to find potential collaborators who share your
interests.

You may receive significant help from students on other teams (even
sharing code!), as long as (a) they did not choose a very similar
topic for their project, and (b) you cite the help you received.

After you submit your proposal, we'll pair you with another team for
peer feedback on some initial results you'll share with them (one
visualization accompanied by some text).  Getting started on a project
is the hardest part, so the goal here is to force every team to make
that first plot early.

For other CS 320 projects, you are never allowed to post your work
publicly online, even after the semester ends.  For this final "exam",
you are allowed to publish your work after the semester ends, but
please don't do so before final grades are released. We don't want
teams working on similar projects to copy your code.

## Proposal

Submit it here by Monday, April 20th: https://forms.gle/3DfVmQeHGdPH4yfUA

This lets us know the topic and who will be collaborating on it.  Only
one team member should submit.

Provides URLs to the data you'll use.  You should rely on at least two
different data files.  There's no upper limit on how many data files
you may use!  Kaggle is not allowed as a source (others have usually
done the hard preprocessing work for those datasets).

Describe the audience for whom you're doing the analysis.  You should
assume your audience is technical (for example, they've taken CS 320),
so this is more about what other background they have and their role
in society.

List some of the questions you want to answer and potential
actions/policies that will be evaluated.  Be sure to tie this to the
audience.  For example, if the audience is Madison's city council,
suggestions related to US federal spending are not relevant.

## Pages

You site should have four pages: index.html, data.html, acks.html, and
results.html (most important).

You may spend time to make the pages aesthetically pleasing if you
like, but we only care about the content for grading purposes.

The requirements for each page are given [here](pages.md).

## Submission

Hand in a `final.zip` file as P7 at the same place you submit regular
projects:
https://tyler.caraza-harter.com/cs320/s20/submission.html. The zip
should contain your code, pages, and graphics.  If the data is small,
include that too (the whole zip must be <1 MB).

Only one team member should submit.  The submission site may complain
about missing project, submitter, and partner info.  The site doesn't
support multiple partners (as allowed for the final), so please just
check the "Ignore Errors" box this time.

We should be able to perform the following steps to evaluate your work
(test it for yourself before handing in!):

1. `unzip final.zip`
2. `cd final`
3. `python3 -m http.server --bind 127.0.0.1 8000`
4. open `http://127.0.0.1:8000/index.html` in a web browser

_*Note*_: The above is for testing out your submission locally. To do this on your VM, replace `127.0.0.1` by `0.0.0.0` in step 3 and in step 4, replace `127.0.0.1` with your VM's IP address. 

Please read the [grading standards](grading.md) carefully.

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
