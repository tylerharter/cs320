# Sep 18 Lecture

## 1. Review Classes and Methods

### Questions

Consider this code, then write answers/guesses on a piece of paper to
the following questions.  We'll go over the answers in the video.

```python
class Dog:
    def init(dog):
        print("created a dog")
        dog.name = name
        dog.age = age
        
    def speak(dog, mult):
        print(dog.name + ": " + "bark!")

fido = Dog()
```

1. which one is an attribute?  `dog`, `name`, `mult`, or `fido`
2. is anything printed?  Does the code crash?

For the rest of the questions , assume `init(dog)` is replaced with `__init__(dog, name, age)` and `Dog()` is replaced with `Dog("Fido", 9)`

3. is anything printed now?  Does the code crash?

Now consider the following method calls:

```python
speak(fido, 5)            # 1
fido.speak(5)             # 2
Dog.speak(fido, 5)        # 3
type(fido).speak(fido, 5) # 4
```

4. Pair each of the following descriptions with one of the above calls:
a. type-based dispatch, bad style
b. type-based dispatch, good style
c. not type-based dispatch, but works
d. crashes

5. if we call `fido.speak(5)`, what will be passed to the `dog` parameter?

6. `dog` is special: it is the receiver, the first parameter of a method.  What is a better parameter name to use instead of `dog`?

### Watch: [10-minute video](https://youtu.be/ggFeAeq3Xww)

## 2. String Representations

### Watch: [20-minute video](https://youtu.be/FkL04j95x0g)

Complete the following  code in a cell:

```python
class ShoppingList:
    def __init__(self, items=[]):
        self.items = items # items we need to get
        self.added = set() # items already in cart
    
    def pickup(????, ????):
        self.added.add(item)
    
    def ????(self):
        s = "<h3>Shopping List</h3><ul>"
        for item in self.items:
            if not item in self.added:
                s += "<li>" + item
            else:
                ????
        s += "</ul>"
        return s
    
slist = ShoppingList(["eggs", "milk", "cookies", "bread"])
slist.pickup("eggs")
slist.pickup("bread")
slist
```

The goal is see a bulleted list with some items crossed off, like this:

<img src="shopping.png">

Hint: the HTML for something crossed off is like this: `<del>crossed-out text</del>`

## 3. \_\_getitem\_\_

### Watch: [21-minute video](https://youtu.be/9uRj-kccMm4)
