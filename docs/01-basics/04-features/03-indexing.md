# Indexing feature in Class

To add indexing functionality (like `obj[i]`) to a Python class, you need to implement the **`__getitem__`** method in your class. Optionally, you can also implement **`__setitem__`** and **`__delitem__`** to handle assignment and deletion of items.

---

## Read indexing

```python
class MyList:
    def __init__(self, data):
        self.data = data  # Store the data in an internal list

    def __getitem__(self, index):
        return self.data[index]  # Use the internal list's indexing

# Example usage
obj = MyList([10, 20, 30, 40])
print(obj[1])  # Outputs: 20
```

---

## Write indexing

```python
class MyList:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value  # Allow modification of the internal list

# Example usage
obj = MyList([10, 20, 30, 40])
print(obj[1])  # Outputs: 20
obj[1] = 99    # Updates the second element
print(obj[1])  # Outputs: 99
```

---

## Deletion at index

```python
class MyList:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __delitem__(self, index):
        del self.data[index]  # Remove the specified element

# Example usage
obj = MyList([10, 20, 30, 40])
print(obj[1])  # Outputs: 20
del obj[1]     # Deletes the second element
print(obj.data)  # Outputs: [10, 30, 40]
```

---

## Support for Slicing

```python
if isinstance(index, slice):
    ...
```

If you want your class to support slicing (e.g., `obj[1:3]`), you can handle this in the **`__getitem__`**, **`__setitem__`**, and **`__delitem__`** methods by checking if the `index` is a slice.

```python
class MyList:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        if isinstance(index, slice):
            print("index is a slice", index)
        return self.data[index]  # Handles both single index and slicing

    def __setitem__(self, index, value):
        self.data[index] = value  # Handles both single index and slicing

    def __delitem__(self, index):
        del self.data[index]  # Handles both single index and slicing

# Example usage
obj = MyList([10, 20, 30, 40, 50])
print(obj[1:4])  # Outputs: [20, 30, 40]
obj[1:3] = [99, 100]  # Updates a slice
print(obj.data)  # Outputs: [10, 99, 100, 40, 50]
```

---

## Summary

1. Implement **`__getitem__`** for read-only access (`obj[i]`).
2. Implement **`__setitem__`** for assignment (`obj[i] = value`).
3. Implement **`__delitem__`** for deletion (`del obj[i]`).
4. Handle slicing by leveraging the fact that `index` can be a `slice` object.
