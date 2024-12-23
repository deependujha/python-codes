# Concurrent.futures in Python

- High level API for asynchronously executing callables
- Provides:
    - Base class: **Executor**
    - **ThreadPool Executor**
    - **ProcessPool Executor**

---

## Executor class

- **Executor** class is an abstract class that provides methods to execute callables asynchronously
- It provides two methods:
    - **submit()**: Schedules the callable to be executed and returns a **Future** object
    - **map()**: Maps the callable to an iterable of callables and returns a generator of **Future** objects.

- `future` object is returned by them. It represents the result of the asynchronous computation.
- `map()` function's future returns value in the order of the input iterable.
- `submit() + as_completed` function's future returns value in the order of completion.

---

## Code Example

- `submit() + as_completed()`

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def task(n):
    time.sleep(n)
    return n * n

if __name__ == "__main__":
    inputs = [3, 1, 4]
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(task, n) for n in inputs]
        for future in as_completed(futures):
            print(future.result())  # Output could be unordered: 1, 9, 16
```

- `map()`

```python
from concurrent.futures import ThreadPoolExecutor
import time

def task(n):
    time.sleep(n)  # Simulate variable execution time
    return n * n

if __name__ == "__main__":
    inputs = [3, 1, 4]
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(task, inputs)  # Results will be in the order of `inputs`

    for result in results:
        print(result)  # Output: [9, 1, 16]
```
