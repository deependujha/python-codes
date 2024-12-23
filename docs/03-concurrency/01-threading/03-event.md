# Event in Threading

- **communication mechanism b/w threads**

!!! quote ""
    one thread signals an event and other threads wait for it.

!!! success ""
    An event object manages an **internal flag** that can be:

    - set to `true` with the `set() method`
    - `is_set()` return True if and only if the internal flag is true.
    - and `reset` to false with the `clear() method`.
    - The `wait(timeout=None)` method **blocks** until the flag is true.
    - If timeout of wait is not None (a floating point), it will wait for the flag to be set for the specified time, and then return `True` if the flag is set, otherwise `False`.

---

## Code

- A sample code:

```python
from threading import Thread, Event
import time
import threading

# Create an Event object
event = Event()

# Function that waits for the event to be set
def worker():
    print(f"Worker is waiting for the event...{event.is_set()=}")
    event.wait()  # Wait until the event is set
    print(f"Worker is proceeding! {event.is_set=}")

# Start a thread that runs the worker function
thread = Thread(target=worker)
thread.start()

# Simulate some delay
time.sleep(2)
print("Main thread setting the event!")
event.set()  # Signal the worker to proceed
```
