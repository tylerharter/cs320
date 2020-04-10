# April 15 Lecture

## 1. Parallelism

### Watch: [23-minute video](https://youtu.be/gQMcyW7baPE)

### Practice: Questions

What is an advantage of GPUs over CPUs?
1. the cores are more flexible
2. the cores are faster
3. there are more cores overall

<details>
    <summary>ANSWER</summary>
    (3) GPUs generally have many more cores, but they are typically slower and less flexible
</details>

In what pattern are there multiple instruction pointers executing different code in the same process?
1. thread parallelism
2. process parallelism
3. GPU parallelism

<details>
    <summary>ANSWER</summary>
    (1) each instruction pointer is associated with a thread, and thread parallelism means there are multiple threads in the same process
</details>


## 2. Pool Map

### Watch: [10-minute video](https://youtu.be/O2xCQGmMQtA)

### Practice: String Mult

Consider this code:

```python
nums = [2, 1, 8]
laughs = ["ha"*must for must in nums]
laughs
```

Finish the following to achieve the same result, but with the help of
a pool of 5 processes:

```python
from multiprocessing.pool import Pool

def laugh(mult):
    return ????

with Pool(????) as p:
    laughs = p.map(????, nums)

laughs
```

<details>
    <summary>ANSWER</summary>
    Replace the blanks with <code>"ha"*mult</code>, <code>5</code>, and <code>laugh</code>
</details>


## 3. Parallel Download

### Watch: [6-minute video](https://youtu.be/kfEISnytm1E)

### Practice: Pool Size


## 4. Debugging

### Watch: [10-minute video](https://youtu.be/cGQfl5Od25s)

### Practice: ????


# Remember!

Please record that you finished this lecture: https://forms.gle/z9oCk4BzvVjdN1aZ6
