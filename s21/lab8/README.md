# Lab 8: Smile!

You may have heard that [face-recognition
systems](https://en.wikipedia.org/wiki/Facial_recognition_system) are
a big deal in machine learning.

In this project, you'll build your very own face recognition system,
at least by some definitions. ;)

Your job is to detect smileys in the following text (nonsense text
adapted from https://en.wikipedia.org/wiki/Lorem_ipsum, with smileys
added by instructor).

```python
s = """Lorem ipsum dolor sit amet ;), consectetur adipiscing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. :) Ut enim ad
minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. :( :( :( Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum. :P

Curabitur pretium tincidunt lacus. :-) Nulla gravida orci a odio. :P Nullam
varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus
magna felis sollicitudin mauris. ;-) Integer in mauris eu nibh euismod
gravida. Duis ac tellus et risus vulputate vehicula. Donec lobortis
risus a elit. Etiam tempor. :-( Ut ullamcorper, ligula eu tempor congue,
eros est euismod turpis, id tincidunt sapien risus a quam. :) Maecenas
fermentum consequat mi. Donec fermentum. Pellentesque malesuada nulla
a mi. :) Duis sapien sem, aliquet nec, commodo eget, consequat quis,
neque. Aliquam faucibus, elit ut dictum aliquet, felis nisl adipiscing
sapien, sed malesuada diam lacus eget erat. :/ Cras mollis scelerisque
nunc. Nullam arcu. ;-) Aliquam consequat. Curabitur augue lorem, dapibus
quis, laoreet et, pretium ac, nisi. :) Aenean magna nisl, mollis quis,
molestie eu, feugiat in, orci. In hac habitasse platea dictumst. :/"""
```

Paste it to a notebook.

# Getting the Regex Right

Run the following:

```python
import re

# from DS100 book...
def reg(regex, text):
    """
    Prints the string with the regex match highlighted.
    """
    print(re.sub(f'({regex})', r'\033[1;30;43m\1\033[m', text))
    
reg(r":\)", s)
```

You should see something like this:

<img src="regex1.png" width=600>

Your job is to improve the regular expression so that you can match
all the faces!  Use character classes to match different kinds of eyes
and mouths, and use `?` to make noses optional.  If you need to review
these features, go back to the regex reading:
https://www.textbook.ds100.org/ch/08/text_intro.html

Be careful, because many characters used in faces have special meaning
in regexes.  You might need to escape some of these with `\`.

If you're successful, it will look like this:

<img src="regex2.png" width=600>

# Counting Faces

Now use your regex and some more code to count different types of faces:

```python
import pandas as pd

counts = {}
for face in re.findall("????", s):
    ???? # might need a few lines here

pd.Series(counts).sort_values().plot.barh(fontsize=20, color="k")
```

<img src="faces.png" width=400>

# Optional Challenge: Making Everybody Happy

Can you use `re.sub` to make all the mouths happy (i.e., `)`)?  You'll
need to use `\g<N>` to keep the eyes and nose the same while replacing
the mouths.