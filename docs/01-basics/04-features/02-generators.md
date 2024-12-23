# Generators

## Overview

- **`Generators`** are a simple and powerful tool for creating `iterators`.
- They are written like regular functions but use the **`yield`** statement whenever they want to return data.
- Each time **`next()`** is called on it, the generator resumes where it left off (it remembers all the data values and which statement was last executed).
- When it terminates, it raises **`StopIteration`** exception.

```python
>>> def reverse(data):
...    for index in range(len(data)-1, -1, -1):
...        yield data[index]
>>>
>>> for char in reverse('golf'):
...    print(char)
f
l
o
g
```

!!! success ""
    - Anything that can be done with generators can also be done with class-based iterators as described in the previous section.
    - What makes generators so compact is that the `__iter__()` and `__next__()` methods are created automatically.

- List comprehension:

```python
>>> [x**2 for x in range(10)] # list comprehension
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> (x**2 for x in range(10)) # list comprehension
<generator object <genexpr> at 0x10c90e650>
```

- To convert a generator to a list, use the `list()` function.
- `all()` and `any()` functions can be used to check if all or any of the elements in a generator are true.

```python
>>> list((x**2 for x in range(10)))
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> all((x**2>0 for x in range(10)))
True
```

- `all((...generator))` and `any((...generator))` can also be used with `all([...list])` and `any([...list])`.

- But, generators will be more efficient than lists when the condition is more complex and the list is very long.

---

## Code

```python
def fib(n):
    a, b = 0, 1
    while n > 0:
        yield a
        a, b = b, a + b
        n -= 1

fib_gen = fib(10)
print(f"{fib_gen=}")

for i in fib_gen:
    print(i)
```
