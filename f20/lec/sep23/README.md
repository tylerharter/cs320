# Sep 23 Lecture

## 1. Review Inheritance

### Watch: [12-minute video](https://youtu.be/jkZeHqy8X-U)

## 2. Multiple Inheritance

### Watch: [21-minute video](https://youtu.be/VhHYsSD_-jM)

When we call `obj.f()` and multiple classes in the hierarchy have a
method `f`, we have the following rules for determining the order in
which we consider classes:

1. prefer descendants
2. prefer closer
3. prefer left

Order these rules from strongest to weakest.

<details>
    <summary>ANSWER</summary>
    <p>
    prefer descendants, prefer left, prefer closer
    </p>
</details>

## 3. Recursion

### Watch: [16-minute video](https://youtu.be/a4YgHmR-A4c)

### Practice:

On paper, trace through what the following prints.  Then run it to check your answer.

```python
def revprint(s):
  if len(s) > 0:
    revprint(s[1:])
    print(s[0])
revprint("ABC")
```
