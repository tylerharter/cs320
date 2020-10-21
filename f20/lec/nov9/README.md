# Nov 9 Lecture

## 1. Vector Multiplication

### Watch: [23-minute video](https://youtu.be/r4B812a6e_0)

### Practice: Vector dot Vector

For the practices, it's probably convenient to disable output scrolling:

<img src="scroll.png" width=400>

Run the following to practice computing the dot product yourself,
until you can get 5 in a row correct:

```python
def practice():
    size = np.random.randint(1,5)
    a = np.random.randint(-3,4,size).reshape(-1,1)
    b = np.random.randint(-3,4,size).reshape(-1,1)
    print("a = ")
    print(a)
    print()
    print("b = ")
    print(b)
    print()
    answer = int(input("What is np.dot(a.T,b), as a scalar?  "))
    print()
    expected = np.dot(a.T, b)[0][0]
    if answer == expected:
        print("Good job!")
        return True
    else:
        print("\nActually, it is ", expected)
        print("Calculation:", " + ".join(f"({x}*{y})" for x,y in zip(a.reshape(-1), b.reshape(-1))))
        time.sleep(2)
        return False

goal = 5
correct = 0
while correct < goal:
    print("="*40)
    print(f"Get {goal-correct} in a row correct to finish!")
    print("="*40)
    print()
    if practice():
        correct += 1
    else:
        correct = 0
    print()
        
print(f"Nice, you got {goal} in a row correct!")
```

## 2. Applications, Matrix Multiplication

### Watch: [15-minute video](https://youtu.be/zCKfjZq2cR8)

### Practice: Matrix dot Vector

Run and practice the following until you can get three in a row.

So this doesn't get tedious, we only make you find one number in the
resulting vector, though you should be able to compute the whole
vector if asked.

To compute a single 'x' value, you'll need to look at all the values
in the vector `b`, but you'll only need to look at a single row of `A`
(you can ignore the other rows).  So your first step should be to
identify that row, based on what row 'x' is in.

```python
def practice(cols):
    rows = np.random.randint(3, 7)
    A = np.random.randint(-3,4,(rows, cols))
    b = np.random.randint(-3,4,cols).reshape(-1,1)
    print("A = ")
    print(A)
    print()
    print("b = ")
    print(b)
    print()
    M = np.dot(A,b).astype(object)
    pos = np.random.randint(0,rows)
    expected, M[pos,0] = M[pos,0], "x"
    print("np.dot(A,b) = ")
    print(M)    
    print()
    answer = int(input("What is 'x'?  "))
    print()
    if answer == expected:
        print("Good job!")
        return True
    else:
        print("\nActually, it is ", expected)
        print("Calculation:", " + ".join(f"({x}*{y})" for x,y in zip(A[pos].reshape(-1), b.reshape(-1))))
        time.sleep(2)
        return False

goal = 3
correct = 0
while correct < goal:
    print("="*40)
    print(f"Get {goal-correct} in a row correct to finish!")
    print("="*40)
    print()
    if practice(correct+2):
        correct += 1
    else:
        correct = 0
    print()
        
print(f"Nice, you got {goal} in a row correct!")
```

## 3. Solving Equations

### Watch: [13-minute video](https://youtu.be/zCKfjZq2cR8)

### Practice: Pricing Fruits

Say you're running an auction selling fruit baskets.  The baskets
contain apples and bananas.

The baskets are pretty cool, so people would pay something even for an
empty basket (even though they are never for sale individually).

You want to put a dollar value on apples, bananas, and baskets.

Let's say you've sold three baskets:

* 10 apples and 0 bananas sold for $7
* 2 apples and 8 bananas sold for $5
* 4 apples and 4 bananas sold for $5

This data gives us three variables and three equations:

* `10*apple + basket == 7`
* `2*apple + 8*banana + basket == 5`
* `4*apple + 4*banana + basket == 5`

Complete the following to find the individual value of each item:

```python
import numpy as np

X = np.array([
    [10,0,1],
    [???,8,1],
    [4,4,???],
])
y = np.array([7,5,???]).reshape(-1,1)

c = np.linalg.solve(X, y)
apple_val, banana_val, basket_val = c.reshape(-1)

print("Apple Value:", apple_val)
print("Banana Value:", banana_val)
print("Basket Value:", basket_val)
```

<details>
    <summary>ANSWER</summary>
    Apples are worth $0.50; bananas, $0.25; baskets, $2
</details>
