# Sep 16 Lecture

## 1. TODO

### Watch: [-minute video]()

## 2. Object Oriented Programming

### Watch: [24-minute video](https://youtu.be/7Rw1uBoJXxw)

### Explore

Copy, paste, and run the example from lecture:

```python
class Dog:
    def speak(dog):
        if dog.age < 2:
            print(dog.name, "bark! " * 5)
        elif dog.age > 10:
            print(dog.name, "grrrr")
        else:
            print(dog.name, "bark")

# NOT GREAT
def init(dog, name, age):
    dog.name = name
    dog.age = age
        
class Cat:
    def speak(cat):
        print("meow")

dog1 = Dog()
init(dog1, "Fido", 1)
dog2 = Dog()
init(dog2, "Sam", 12)
c1 = Cat()

# BAD
Dog.speak(dog1)

Cat.speak(dog1) # dogs don't say "meow"!!!
```

When we run the Cat version of speak on a dog, the dog says something
unexpected.  Switch it: what happens when you call the Dog version of
speak on a cat object (like `c1`)?

## 3. Methods

### Watch: [16-minute video](https://youtu.be/xulHeIkKeyM)
