# Loops and Functions

## Loops

```python
# for loop with range, enumerate, zip
for i in range(10):
    print(i)

for i, j in enumerate(['a', 'b', 'c']):
    print(i, j)

for i, j in zip(['a', 'b', 'c'], ['x', 'y', 'z']):
    print(i, j)
```

## Range

```python
x = range(10)
print(list(x))

x = range(10, 20)
print(list(x))

x = range(10, 20, 2)
print(list(x))
```

## Functions

```python
def add(a, b):
    return a + b

add(1, 2)
```

## Lambda

```python
square = lambda x: x * x
square(2)
```

## `*args` and `**kwargs`

```python
def add(*args):
    return sum(args)

def sub(**kwargs):
    print(kwargs)

add(1, 2, 3, 4, 5)

sub(a=1, b=2, c=3)

my_dict = {'a': 1, 'b': 2, 'c': 3}
sub(**my_dict)
```

## 🚀 Controlling Function Arguments with `*` and `/`

!!! success "What are `*` and `/`?"
    - `/` (Positional-Only Arguments):
        - Arguments before / must be passed positionally (not as keyword arguments).
    - `*` (Keyword-Only Arguments):
        - Arguments after * must be passed as keyword arguments.

```python
def func(a, b, /, c, d):
    print(a, b, c, d)

func(1, 2, c=3, d=4)  # ✅ Works
func(a=1, b=2, c=3, d=4)  # ❌ Error: a and b must be positional

# ===============================

def func(a, b, *, c, d):
    print(a, b, c, d)

func(1, 2, c=3, d=4)  # ✅ Works
func(1, 2, 3, 4)  # ❌ Error: c and d must be keyword arguments

# ===============================

def configure(x, y, /, z, *, verbose=False):
    print(f"x: {x}, y: {y}, z: {z}, verbose: {verbose}")

configure(1, 2, 3, verbose=True)  # ✅ Works
configure(1, 2, z=3, verbose=True)  # ✅ Works
configure(x=1, y=2, z=3, verbose=True)  # ❌ Error: x and y must be positional
configure(1, 2, 3, True)  # ❌ Error: verbose must be keyword-only
```
