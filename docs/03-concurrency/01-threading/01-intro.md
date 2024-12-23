# Multithreading in Python

## Threads

- Smallest unit of execution
- A process can have multiple threads

---

## Types of threads

1. **Main Thread**  : The initial thread of execution when the program starts.
2. **Daemon Threads**  : Background threads that automatically exit when the main thread terminates.
3. **Non-Daemon Threads**  : Threads that continue to run until they complete their task, even if the main thread exits.

---

## Simple `threading` code

!!! info
    - `target` is the function to be executed
    - `args` is the argument to be passed to the function
    - `start` starts the thread
    - `join` waits for the thread to finish

```python
import threading


def print_cube(num):
    print("Cube: {}" .format(num * num * num))


def print_square(num):
    print("Square: {}" .format(num * num))


if __name__ =="__main__":
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,), daemon=True) # daemon thread

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Done!")

```

---

## Daemon Threads

- By passing `daemon=True` to the thread, we can make it a daemon thread.
- Daemon threads are background threads that automatically exit when the main thread terminates.
- Since daemon threads are abruptly terminated when the program ends, they may not finish their work or clean up resources properly. So, they are ideal for tasks that don't require cleanup or finishing. (like `logging`, `monitoring`, etc.)

---

## Thread's name & PID

- all the threads that we will create, will have the same PID.

```python
import threading
import os

def task1():
    print("Task 1 assigned to thread: {}".format(threading.current_thread().name))
    print("ID of process running task 1: {}".format(os.getpid()))

def task2():
    print("Task 2 assigned to thread: {}".format(threading.current_thread().name))
    print("ID of process running task 2: {}".format(os.getpid()))

if __name__ == "__main__":

    print("ID of process running main program: {}".format(os.getpid()))

    print("Main thread name: {}".format(threading.current_thread().name))

    t1 = threading.Thread(target=task1, name='t1')
    t2 = threading.Thread(target=task2, name='t2')

    t1.start()
    t2.start()

    t1.join()
    t2.join()
```

![multithreading](../../images/multithreading/multithreading-python.png)

---

## Simple methods of `threading` module

- `active_count()` : Returns the number of Thread objects currently alive.
- `current_thread()` : Returns the current Thread object, corresponding to the caller's thread of control.
- `enumerate()` : Returns a list of all Thread objects currently alive.
- `main_thread()` : Returns the main Thread object.

```python
import threading

print("Number of active threads: {}".format(threading.active_count()))
print("Current thread: {}".format(threading.current_thread()))
print("List of all threads: {}".format(threading.enumerate()))
print("Main thread: {}".format(threading.main_thread()))
```
