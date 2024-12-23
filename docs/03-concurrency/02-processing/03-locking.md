# Locking & Event in Multiprocessing

## Lock

- `Lock` is a synchronization primitive that allows only one process to access a shared resource at a time.
- it has two methods `acquire(block=True, timeout=None)` and `release()`.

```python
from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()
```

## Lock with context manager

- Lock can also be used as a context manager.
- It automatically acquires the lock before the block and releases it after the block.

```python
from multiprocessing import Process, Lock

def f(l, i):
    with l:
        print('hello world', i)

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()
```

---

## Event

- Similar to threading, `Event` is a communication mechanism between processes.
- one process signals an event and other process wait for it.

!!! success ""
    An event object manages an **internal flag** that can be:

    - set to `true` with the `set() method`
    - `is_set()` return True if and only if the internal flag is true.
    - and `reset` to false with the `clear() method`.
    - The `wait(timeout=None)` method **blocks** until the flag is true.
    - If timeout of wait is not None (a floating point), it will wait for the flag to be set for the specified time, and then return `True` if the flag is set, otherwise `False`.

---

## Event object in multiprocessing are not shared b/w processes ❌👇🏻

```python
from multiprocessing import Process, Event
import time
import multiprocessing

# Create an Event object
event = Event()

# Function that waits for the event to be set
def worker():
    print(f"Worker is waiting for the event...{event.is_set()=}")
    event.wait()  # Wait until the event is set
    print(f"Worker is proceeding! {event.is_set=}")

# Start a thread that runs the worker function
p = Process(target=worker)
p.start()

# Simulate some delay
time.sleep(2)
print("Main thread setting the event!")
event.set()  # Signal the worker to proceed
```

!!! danger "Event object in multiprocessing are not shared b/w processes"
    The above code will not work as expected. The event object is not shared between processes. The worker process will not be able to see the event set by the main process.

    - We need to use `manager.Event()` to create an event object that is shared between processes.

---

## Multiprocessing manager

```python
from multiprocessing import Process, Event, Manager
import time

def worker(event):
    print(f"Worker is waiting for the event...{event.is_set()=}")
    event.wait()  # Wait until the event is set
    print(f"Worker is proceeding! {event.is_set()=}")

if __name__ == "__main__":
    with Manager() as manager:
        # Create a shared Event object
        event = manager.Event()

        # Start a process that runs the worker function
        p = Process(target=worker, args=(event,))
        p.start()

        # Simulate some delay
        time.sleep(2)
        print("Main process setting the event!")
        event.set()  # Signal the worker to proceed
        p.join()
```
