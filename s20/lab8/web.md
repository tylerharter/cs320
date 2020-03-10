# Web+Regex

## Web

In this example, you'll run a simple K/V Store server (this is a
fancy name for a server that basically stores the equivalent of a
Python `dict` and allows other computers to get and set values
associated with keys -- K/V stands for Key/Value).

Create the following app on your virtual machine and run it:

```python
from flask import Flask, request

app = Flask(__name__)

data = {}

@app.route('/')
def lookup():
    key = request.args.get("key", "") # (1) query string
    value = data.get(key, "")
    print(data)
    return value + "\n" # (3) response body

@app.route('/', methods=["POST"])
def put():
    key = request.args.get("key") # (1) query string
    value = request.get_data(as_text=True) # (2) request body
    data[key] = value
    print(data)
    return "success\n" # (3) response body

if __name__ == '__main__':
    app.run(host="0.0.0.0")
```

Notice the three ways data gets into and out of the app:
1. in the query string ("a=apple" is the query string in the URL "http://my-ip:5000?a=apple" -- the part after the "?").  In this example, the keys in the K/V are passed in the query string
2. in the `put` function (which is associated with the POST method), the request also has a body; this is used to upload values to put into the dictionary
3. the response body (the returned value) is used to return values when somebody looks up a key

Try running the following curl command, replacing `my-ip` with the one for your VM:

```
curl -X POST http://my-ip:5000?key=a -d "apple"
```

Here, `curl` issues a POST request (that will go to `put()`).
`request.args` will capture the assignments in the query string, and
will be `{"key": "a"}`.  The part after `-d` will be uploaded as the
request body, and will be retrieved on the server side with
`request.get_data(as_text=True)`.

Let's try getting our value back, now:

```
curl http://my-ip:5000?key=a
```

Here, we should get "apple" back.  We don't specify the method, and
"GET" is the default, so this will go to the `lookup()` method, which
returns the value associated with the specified key in the response
body.

Try inserting some more values:

```
curl -X POST http://my-ip:5000?key=b -d "bananana"
curl -X POST http://my-ip:5000?key=c -d "carrot"
```

And looking them up:

```
curl http://my-ip:5000?key=b
curl http://my-ip:5000?key=c
```

The advantage of using a K/V store over a regular `dict` is that this
dictionary can be shared between users on different computers.  Try
it!  Ask a friend to set a key from their computer, then try looking
it up on yours.

Quiz:

1. if the query string is "?a=b&c=d", what will `request.args` be? <details><summary>Answer</summary><pre>{"a": "b", "c": "d"}</pre></details>

2. What does `request.get_data(as_text=True)` gives access to?  (a) query string, (b) request body, (c) response body <details><summary>Answer</summary>(c) response body</details>

3. The request was sent with `curl -X POST http://my-ip:5000?x=1&y=2&key=hello -d "world"`.  What will `request.args["key"]` be? <details><summary>Answer</summary>"hello"</details>

4. In the above request, what will `request.get_data(as_text=True)` be? <details><summary>Answer</summary>"world"</details>

## Regex

Copy/paste the following:

```python
import re

# from DS100 book...
def reg(regex, text):
    """
    Prints the string with the regex match highlighted.
    """
    print(re.sub(f'({regex})', r'\033[1;30;43m\1\033[m', text))
```

1. Modify the regex so that it only matches the word "the" (or "The")
at the beginning of a string:

```
reg(r"the", "the quick brown fox jumped over the lazy dog.")
```

<details>
<summary>Answer</summary>
<pre>r"^the"</pre>
</details>

2. Modify the regex so that it only matches the last number (in this
case, "789"):

```python
for x in re.findall(r"\d+", "123 456 789"):
    print(int(x))
```

<details>
<summary>Answer</summary>
<pre>r"\d+$"</pre>
</details>

3. How many words have a letter after a "q" that is not a "u"?

For this one, we need to install a list of words.  Run this on the
terminal:

```
sudo apt install wamerican
```

This creates a file named `/usr/share/dict/american-english` with one
word per line.  Take a look:

```
cat /usr/share/dict/american-english
```

Back to the notebook, run this to find how many words contain "qu" in
the dataset:

```python
with open("/usr/share/dict/american-english") as f:
    words = f.read().lower()

qu = re.findall("\w*qu\w*", words)
print(qu[:10])
len(qu)
```

Now tweak the above example so that it counts words with a "q"
followed by something other than a "u".

<details>
<summary>Answer</summary>
<pre>r"\w*q[^u\s]\w*"</pre>
</details>

