# Page 1 - index.html

The home page should include title, names, wiscmail addresses,
 one-paragraph summary of the project, and links to the other pages (listed below).

# Page 2 - data.html

Describe the original data files you're using and the columns in any
tables.  You may quote other documentation if you like (put in quotes
and include a link), but it's your responsibility to make sure this
documentation isn't ambiguous, so either (a) avoid using any data
fields you don't understand or (b) dig deeper until you can write
better documentation than what's in the original.

If the data is too large to include in final.zip, include directions
(code snippets, bash commands, etc) on how to grab the data.

# Page 3 - acks.html

This acknowledgments page should list any people or online resources
you used to complete your project.

There's no specific format required, but be comprehensive.

You don't need to cite help from your instructor or TAs.

We'll be doing a round of peer feedback on a single plot and some
accompanying text.  Plots will be sent by Apr 24 and feedback by Apr
27.  The ack page should contain a before/after version of this
content, along with the peer feedback (so we can see how you
integrated the suggestions).

# Page 4 - results.html

This page should have visuals interleaved with text.

## Including Graphics in HTML

You can include visuals in your page by running a snippet like this in
your Python code:

```python
ax.get_figure().savefig("fig1.svg", bbox_inches="tight")
```

Then including some HTML like this in results.html:

```html
<img src="fig1.svg" width=600>
```

Or, for animations, you may paste the output from `.to_html5_video()`
directly into your results.html.

If you use visualization tools beyond what we learned in class, they
shouldn't depend on any online resources each time they're displayed
I'm specifically thinking of folium, which I dislike because it
re-fetches map data every time a map is shown, but this applies to any
tool that behaves this way.

## Guidelines for Visuals

Your results.html page should have exactly 10 visualizations (mostly
plots, but also maps and animations).  These 10 should include at least
one of each of the following:

1. stacked or clustered bar plot
2. line plot with multiple lines
3. scatter plot with a regression line showing a correlation between two variables
4. scatter plot with multiple markers representing different categories
5. geographic map
6. animation (max 30 seconds long)

Notice that you have 4 plots remaining where you can pick the style
yourself -- or perhaps more, if you satisfy multiple requirements with
the same plot (for example, you could satisfy the last two with a
single animated map).

You may choose to have multiple subplots in the same figure (for
example, with `plt.subplots(ncols=2)`) -- the whole thing will count
as one visualization towards your count of 10.  This is discouraged as
a means to squeeze in more plots.  It's encouraged if you text is
highlighting interesting comparisons across the subplots.

An important grading criterion is that you identify use cases where
each of the above is the best form of visualization.  For example,
using a clustered bar plot where a stacked one would be more
appropriate would not receive a good score.  Consider reviewing this:
https://tyler.caraza-harter.com/cs301/fall19/readings/axes.html#Picking-the-Right-Plot.

As another example of the wrong visualization being used, here's a
horrible animated bar plot:
https://www.reddit.com/r/dataisbeautiful/comments/fumbza/oc_coronavirus_covid19_daily_cases_by_country_per/.
A simple plot with time on the x-axis and one line per country would
have saved audience time and made the trends more apparent.  Being
informative matters, being flashy doesn't.  You're more than welcome
to make all visuals gray scale if you like.

## Guidelines for Text

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
followup question, then actually followup in the next plot if you can.
Don't leave the reader hanging!

Use the text to connect one plot to the next, or to give a preview of
why different plots will go in different sections.