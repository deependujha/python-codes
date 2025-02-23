# Dictionaries & Sets in Python

## Dictionaries

Dictionaries store key-value pairs and are **mutable**.

### Creating Dictionaries

```python
dct = {'a': 1, 'b': 2, 'c': 3}
empty_dct = {}
dict_from_pairs = dict([('a', 1), ('b', 2)])
```

### Accessing & Modifying

```python
value = dct['a']           # Access value
dct['d'] = 4              # Add new key-value pair
dct['a'] = 10             # Modify value
del dct['b']              # Delete key-value pair
```

### Dictionary Methods

```python
keys = dct.keys()          # Get all keys
values = dct.values()      # Get all values
items = dct.items()        # Get key-value pairs
default = dct.get('x', 0)  # Get with default

# loop through dict
for key, value in dct.items():
    print(key, value)

# check if key exists in dict
if 'x' in dct:
    print(dct['x'])
else:
    print('x not found')
```

### DefaultDict

A `defaultdict` provides default values for missing keys.

```python
from collections import defaultdict
dd = defaultdict(int)  # Default value is 0
dd['x'] += 1          # Works without key error

dl = defaultdict(list)
dl['x'].append(1) # Works without key error, creates empty list
```

### OrderedDict

An `OrderedDict` remembers the order of items.

```python
# A Python program to demonstrate working of OrderedDict
from collections import OrderedDict

od = OrderedDict()
od['a'] = 1
od['b'] = 2
od['c'] = 3
od['d'] = 4
od['a'] = 5

for key, value in od.items():
    print(key, value)
```

### Equality in ordered dict

```python
from collections import OrderedDict

# Create two ordered dictionaries with different orderings
od1 = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
od2 = OrderedDict([('c', 3), ('b', 2), ('a', 1)])

# Compare the ordered dictionaries for equality
print(od1 == od2) # False
```

---

## Sets

Sets store **unique** elements and are unordered.

### Creating Sets

```python
s = {1, 2, 3, 4, 5}
empty_set = set()
set_from_list = set([1, 2, 3, 2, 1])  # Removes duplicates
```

### Set Operations

```python
s.add(6)            # Add an element
s.remove(3)         # Remove an element
union = s | {7, 8}  # Union
intersection = s & {2, 4, 6}  # Intersection
difference = s - {1, 2}  # Difference
```

### Membership & Length

```python
length = len(s)     # Get length
exists = 3 in s     # Check membership

# loop through set
for element in s:
    print(element)
```

!!! warning "int v/s tuple v/s set"

    ```python
    v1 = (1) # int
    v2 = (1,) # tuple
    v3 = {1} # set
    ```

---

## Quick Functions Reference

| Operation        | Dictionary               | Set                  |
|-----------------|-------------------------|----------------------|
| Length          | `len(dct)`               | `len(s)`            |
| Access Value    | `dct[key]`               | ❌                   |
| Add Item        | `dct[key] = value`       | `s.add(x)`          |
| Remove Item     | `del dct[key]`           | `s.remove(x)`       |
| Membership      | `key in dct`             | `x in s`            |
| Union          | ❌                         | `s | other_set`     |
| Intersection   | ❌                         | `s & other_set`     |
| Difference     | ❌                         | `s - other_set`     |
