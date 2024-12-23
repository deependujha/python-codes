# Iterators

!!! danger ""
    - Anything that can be done with generators can also be done with class-based iterators.
    - What makes generators so compact is that the `__iter__()` and `__next__()` methods are created automatically.

## Overview

- When we write `for` loop, it internally calls **`iter()`** on the container object.
- The **`iter()`** function returns an **`iterator`** object.
- The **`iterator`** object has a **`__next__()`** method that returns the next item in the container.
- The **`__next__()`** method is called repeatedly until it raises **`StopIteration`** exception, which tells the **`for`** loop to stop iterating.

```python
>>> s = 'abc'
>>> it = iter(s)
>>> it
<str_iterator object at 0x10c90e650>
>>> next(it)
'a'
>>> next(it)
'b'
>>> next(it)
'c'
>>> next(it)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    next(it)
StopIteration
```

---

## Code

```python
class Reverse:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index <= 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]

rev = Reverse('abcdef')

for c in rev:
    print(c)
```
