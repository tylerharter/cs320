# Complexity Analysis

## Big O

What is the complexity of appending to a list?

<details>
<summary>Answer</summary>
O(1)
</details>

What is the complexity of popping from the beginning of a list?

<details>
<summary>Answer</summary>
O(N), where N is len(N)
</details>

What is the complexity of merge sort?

<details>
<summary>Answer</summary>
O(N log N), where N is len(N)
</details>

If some code has two steps, the first of which is O(N), and the second
of which is O(N**2), what is the overally complexity of the code?

<details>
<summary>Answer</summary>
O(N ** 2)
</details>

If some code consists of a loop that iterates N times, and the body of
the loop consists of a call to a function with complexity O(N**4),
what the overall complexity of the code?

<details>
<summary>Answer</summary>
O(N ** 5)
</details>

O(N ** 3 + 4 * N ** 2 + 5*N + 10) can be simplified to what?

<details>
<summary>Answer</summary>
O(N ** 3)
</details>

O(N + (N-1) + (N-2) + ... + 2 + 1) can be simplified to what?

<details>
<summary>Answer</summary>
O(N**2)
</details>

## Data Structures

Assume the values 3, 1, 5, 3, 9, and 8 are added to a structures, in
that order.  If a value is then popped from that structure, what will
the value be if the stucture is a:

<details>
<summary>Stack</summary>
8
</details>

<details>
<summary>Queue</summary>
3
</details>

<details>
<summary>Priority Queue</summary>
either 1 or 9, depending on whether smaller or larger is considered higher priority
</details>

## Key Concepts
 * data size
 * what is a "step"?
 * Big O notation
 * complexity of common operations (append, insert, pop, len, etc)
 * stack, queue, priority queue

## Resources
 * https://tyler.caraza-harter.com/cs320/s20/materials/lec-04.pdf
 * http://greenteapress.com/thinkpython2/html/thinkpython2022.html
 * https://tyler.caraza-harter.com/cs320/s20/materials/lec-05-worksheet.key.pdf
 * https://tyler.caraza-harter.com/cs320/s20/materials/lec-05-worksheet-answers.key.pdf
 * https://github.com/tylerharter/cs320/blob/master/s20/lab3/part2.md
 * https://github.com/tylerharter/cs320/blob/master/s20/lab3/part3.md
