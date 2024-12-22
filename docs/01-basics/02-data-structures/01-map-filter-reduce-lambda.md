# Map, Filter, Reduce and Lambda

## Map

- `map` applies a function to all the items in an input list, and returns new list.

```python
def double(x):
    return x * 2

numbers = [1, 2, 3, 4, 5]
doubles = list(map(double, numbers))
print(doubles)  # [2, 4, 6, 8, 10]
```

---

## Filter

- `filter` creates a list of elements for which a function returns `True`.

```python
def is_even(x):
    return x % 2 == 0

numbers = [1, 2, 3, 4, 5]
evens = list(filter(is_even, numbers))
print(evens)  # [2, 4]
```

---

## Reduce

- `reduce` applies a rolling computation to sequential pairs of values in a list.

```python
from functools import reduce

def add(x, y):
    return x + y

numbers = [1, 2, 3, 4, 5]
sum = reduce(add, numbers)
print(sum)  # 15
```

---

## Lambda

- `lambda` is an anonymous function that can have any number of arguments, but can have only one expression.

```python
double = lambda x: x * 2
print(double(5))  # 10
```

---

## Using lambda function with map

```python
numbers = [1, 2, 3, 4, 5]
doubles = list(map(lambda x: x * 2, numbers))
print(doubles)  # [2, 4, 6, 8, 10]
```
