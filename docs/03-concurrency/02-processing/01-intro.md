# Multiprocessing in Python

- Utilize multiple processors to speed up your code
- Escaping the GIL
- `multiprocessing's process` is analogous to `threading's thread`. They hvae similar APIs.

---

## Methods to start new process

`multiprocessing` supports three ways to start a process:

- **Fork**: Creates a new process by copying the parent, making it the fastest but potentially risky due to shared resources (UNIX only). `Fork is fast, potentially unsafe, and may carry unnecessary data from the parent, though Copy-On-Write mitigates this`.
- **Spawn**: Starts a clean process from scratch, ensuring safety and isolation but at the cost of slower startup (default on Windows). `While slower, this is the safest option, especially for long-running or resource-sensitive tasks`.
- **Forkserver**: Uses a dedicated server to spawn processes, combining safety with moderate performance overhead (UNIX only). `Though less commonly used due to setup complexity and limited documentation, it’s useful for controlled multi-process environments`.

---

## Set & Get `process start method`

- To select a start method you use the `set_start_method()` in the if `__name__ == '__main__'` clause of the main module.

```python
import multiprocessing as mp

print(mp.get_start_method())  # Get the current start method

if __name__ == '__main__':
    mp.set_start_method('forkserver')  # Set the start method
```

- **set_start_method()** should not be used more than once in the program.

---

## Simple multiprocessing example

```python
# importing the multiprocessing module
from multiprocessing import Process
import os

def print_cube(num):
    """
    function to print cube of given num
    """
    print("Cube: {}; and {}".format(num * num * num, os.getpid()))

def print_square(num):
    """
    function to print square of given num
    """
    print("Square: {}; and {}".format(num * num, os.getpid()))

if __name__ == "__main__":
    # creating processes
    p1 = Process(target=print_square, args=(10, ))
    p2 = Process(target=print_cube, args=(10, ))

    # starting process 1
    p1.start()
    # starting process 2
    p2.start()

    # wait until process 1 is finished
    p1.join()
    # wait until process 2 is finished
    p2.join()

    # both processes finished
    print("Done!")
```

!!! info
    `Process` has very similar API to `Thread` in `threading` module.

    - `start()`, `join()`, `is_alive()`, etc.
    - `Process` also provides a `terminal()` and `kill()` method to terminate a process.
    - `target` is the function to be executed by the process.
    - `args` is the arguments to be passed to the target function.

![multiprocessing](../../images/multithreading/Multiprocessing-Python.png)
