# Lists & Tuples

## Lists

Lists are **mutable** ordered sequences.

- Creating Lists

```python
lst = [1, 2, 3, 4, 5]
empty_lst = []
list_from_tuple = list((1, 2, 3))
list_from_range = list(range(5))
```

- Lists: Accessing Elements

```python
first = lst[0]      # First element
last = lst[-1]      # Last element
sublist = lst[1:4]  # Slicing (index 1 to 3)
```

- Modifying Lists

```python
lst.append(6)       # Add an element
lst.insert(2, 99)   # Insert at index 2
lst.extend([7, 8])  # Extend list
lst[0] = 0          # Modify element
lst.remove(3)       # Remove element by value
del lst[1]          # Delete by index
```

- Sorting & Reversing

```python
lst.sort()          # Sort in ascending order
lst.sort(reverse=True) # Sort in descending order
lst.reverse()       # Reverse list in place
sorted_lst = sorted(lst) # Returns sorted list without modifying original
```

- Length & Membership

```python
length = len(lst)       # Get length
exists = 3 in lst       # Check membership
```

- List Comprehensions

```python

squares = [x**2 for x in range(10)]
even_nums = [x for x in lst if x % 2 == 0]
```

### Performance Consideration for lists

- Lists consume more memory due to their dynamic nature.
- Slower compared to tuples in iteration.
- Appending (`.append()`) is faster than inserting (`.insert()`).

---

## Tuples

Tuples are **immutable** ordered sequences.

- Creating Tuples

```python
tpl = (1, 2, 3, 4, 5)
single_element_tpl = (42,)  # Comma needed for single element
tuple_from_list = tuple([1, 2, 3])
```

- Tuples: Accessing Elements

```python
first = tpl[0]      # First element
last = tpl[-1]      # Last element
subtuple = tpl[1:4] # Slicing
```

### Named Tuples

Useful for struct-like behavior.

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(p.x, p.y)  # Accessing named attributes
```

### Named tuples with classes

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

p = Point(10, 20)
print(p.x, p.y)  # Accessing named attributes
```

### Tuple methods

- `_asdict()`: Convert to a dictionary.
- `_make()`: Convert a sequence or iterable to a tuple.
- `_replace()`: Return a new tuple with replaced values.
- `_fields()`: Get field names.
- `_field_defaults()`: Get field defaults.

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'], defaults=[0])
p = Point(10, 20)

print(p._asdict())
print(p._make([1, 2]))
print(p._replace(x=100))
print(p._fields)
print(p._field_defaults)
```

### Performance Consideration for tuples

- Tuples use less memory than lists.
- Faster than lists in iteration and lookup.
- Immutable, which makes them **hashable** (can be used as dict keys).

---

## When to Use What?

| Feature       | List          | Tuple        |
|--------------|--------------|-------------|
| Mutability   | Mutable      | Immutable   |
| Performance  | Slower       | Faster      |
| Memory Usage | More         | Less        |
| Use Case     | Dynamic Data | Fixed Data  |

---

## Quick Functions Reference

| Operation        | List                     | Tuple                   |
|-----------------|-------------------------|-------------------------|
| Length          | `len(lst)`               | `len(tpl)`              |
| Sort            | `lst.sort()` for inplace; `sorted(lst)` returns new list            | `sorted(tpl)`           |
| Reverse         | `lst.reverse()`          | `reversed(tpl)`         |
| Append         | `lst.append(x)`          | ❌ (Immutable)          |
| Insert         | `lst.insert(i, x)`       | ❌ (Immutable)          |
| Remove         | `lst.remove(x)`          | ❌ (Immutable)          |
| Membership     | `x in lst`               | `x in tpl`              |
