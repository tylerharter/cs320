# April 1 Lecture

## 1. Pre-Machine Learning Intro

### Watch: [19-minute video](https://youtu.be/ovKsvjKIjB0)

### Practice: Types of Problem

What kind of problem is each of the following?  (a) Supervised ML
(Regression), (b) Supervised ML (Classification), or (c) Unsupervised
Clustering.

1. you want to identify the major demograhpics that have accounts on your website.

<details>
    <summary>ANSWER</summary>
    <code>Unsupervised Clustering</code>
</details>

2. you want to build a system to predict whether a web request is from a bot or human, based on previous data from known bots/humans

<details>
    <summary>ANSWER</summary>
    <code>Supervised (Classification)</code>
</details>

3. you want to build a system from past data to predict how high a river's water level will rise given season, rainfall, etc.

<details>
    <summary>ANSWER</summary>
    <code>Supervised (Regression)</code>
</details>

## 2. Creating Arrays

### Watch: [6-minute video](https://youtu.be/0FWoGHopv9I)

### Practice: Slicing

Copy/paste the following to a cell:

```python
import numpy as np
a = np.arange(10)
b = a[::1]
b
```

Change the step slice above to `-1`.  What does this do to `b`?

Copy/paste the following to a cell:

```python
import numpy as np
a = np.arange(10)
half = a[:5]
# TODO
half[0] += 50
print(a[0])
```

Add some code to replace `#TODO` so that `a` isn't changed, and `0` is
printed.

## 3. Tensors and Images

### Watch: [15-minute video](https://youtu.be/Lml34vUoeCA)

### Practice: Image Manipulation

In order to use `imread`, you need to install the `Pillow` package:

```
pip3 install Pillow
```

Now download the image used during lecture (or feel free to find another one if you like):

```
wget https://upload.wikimedia.org/wikipedia/commons/f/f2/Coccinella_magnifica01.jpg -O bug.jpg
```

#### Crop

Add some numeric ranges to the following to zoom in on the bug (or the
main subject of whatever image you're using):

```python
import matplotlib.pyplot as plt
import numpy as np
a = plt.imread("bug.jpg")
a = a[:, :, :] # TODO
plt.imshow(a)
```

It should look something like this:

<img src="crop.png" width=400>

<details>
    <summary>ANSWER</summary>
    <code>a[700:1600, 400:1600, :]</code>
</details>

#### Resizing

What if we want to use fewer pixels to make a smaller image file?

The following uses a stride of 2 both vertically and horizontally.
Although this means we only keep 1/4 of the original pixels, the
result looks pretty much the same.

```python
a = plt.imread("bug.jpg")
a = a[::2, ::2, :]
plt.imshow(a)
```

What if you only take every 50th pixel (try it by modifying the
strides above!)?  This experiment will show you why programmers always
make fun of crime dramas on TVs where detectives keep zooming in on
images to find tiny clues. :)

<details>
    <summary>RESULT</summary>
    <img src="resize.png" width=400>
</details>


#### Grayscale

Let's say we want to covert a color image to grayscale.  In the
lecture, did something like this: we pulled out red light only
(converting it to grayscale) and ignored green and blue light.

A better way is to average red, green, and blue to determine the shade
of gray.  Run the following:

```python
a = plt.imread("bug.jpg")
a = a.mean()
print(a.shape)
a
```

It's taking an average of all values in the tensor, but we only want
to average over the three colors.  Try passing `axis=N` to the `mean`
method, where `N` is 0, 1, or 2.  Which axis value gives us a
1688x2521 matrix?  Use that one, then show the image with
`plt.imshow(a, cmap="gray")`:

<img src="gray.png" width=400>

<details>
    <summary>ANSWER</summary>
    <code>a.mean(axis=2)</code>
</details>
