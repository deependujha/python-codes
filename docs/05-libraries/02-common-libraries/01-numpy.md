# NumPy - Numerical Python

## Installation

```bash
pip install numpy
```

---

## Creating Arrays

```python
import numpy as np

a = np.array([1, 2, 3])               # 1D array
b = np.array([[1, 2], [3, 4]])        # 2D array

np.zeros((2, 3))                      # All zeros
np.ones((3, 3))                       # All ones
np.eye(3)                             # Identity matrix
np.arange(0, 10, 2)                   # [0, 2, 4, 6, 8]
np.linspace(0, 1, 5)                  # [0. , 0.25, 0.5 , 0.75, 1. ]
```

---

## Array Operations

```python
a + b      # Element-wise addition
a * 2      # Scalar multiplication
a @ b      # Matrix multiplication (or np.dot(a, b))
a.T        # Transpose
a.mean()   # Mean of all elements
a.sum()    # Sum of all elements
a.shape    # Shape of array
a.reshape((2, 3))  # Reshape
```

---

## `np.concatenate`

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])

np.concatenate((a, b), axis=0)  # Vertical stack
np.concatenate((a.T, b.T), axis=1)  # Horizontal stack
```

---

## `np.cumsum` (Cumulative Sum)

```python
a = np.array([1, 2, 3, 4])
np.cumsum(a)  # [ 1  3  6 10 ]

b = np.array([[1, 2], [3, 4]])
np.cumsum(b, axis=0)
# [[1 2]
#  [4 6]]
```

---

## Indexing & Slicing

```python
a[0]           # First element
a[1:3]         # Slice
a[:, 1]        # All rows, 2nd column
a[::2]         # Every other element
a[a > 2]       # Boolean masking
```

---

## Random

```python
np.random.seed(42)                # For reproducibility
np.random.rand(3, 3)              # Uniform [0, 1)
np.random.randn(3, 3)             # Normal distribution
np.random.randint(0, 10, (2, 3))  # Random ints in [0, 10)
```

---

## Useful Utilities

```python
np.unique(a)       # Unique values
np.clip(a, 0, 1)   # Clamp values to [0, 1]
np.sort(a)         # Sort
np.argmax(a)       # Index of max
np.isnan(a)        # Check NaNs
```
