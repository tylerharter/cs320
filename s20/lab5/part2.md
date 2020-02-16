# Part 2: Date Formatting

Copy/paste the following:

```python
from datetime import datetime
fri = datetime(2020, 2, 21)
```

Now run this:

```python
fri.strftime("%d of %b")
```

You should get this output:

```
'21 of Feb'
```

The `strftime` method can format dates in a variety of ways.  `%d` and
`%b` are examples of *format codes*.  You pass a variety of strings
containing format codes to strftime to format dates in a variety of
ways.

Read about the other codes here:

https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

Can you modify the above strftime call to get "21 of Feb, 2020"?

<details>
<summary>Answer</summary>
<pre>
fri.strftime("%d of %b, %Y")
</pre>
</details>

Try other format strings to get these as well:

* "Friday" (P2 hint: note that columns in calendar.txt are named after days of the week)
* "Fri, February 21"
* "2020-02-21"
* "20200221" (P2 hint: note that dates in this format can be converted to integers for easy comparisons with other dates)

Now run the following to get the current time:

```python
now = datetime.now()
```

Try to get formats like the following (note that your exact numbers will be different because your time is after this has been written!):

* "04 PM"
* "16:57:50"
* "16:57:50.960614"
* "16:57:50 on 2020-02-16"
* "20200216165750"

<details>
<summary>Answers</summary>
<pre>
now.strftime("%I %p")
now.strftime("%H:%M:%S")
now.strftime("%H:%M:%S.%f")
now.strftime("%H:%M:%S on %Y-%m-%d")
now.strftime("%Y%m%d%H%M%S")
</pre>
</details>
