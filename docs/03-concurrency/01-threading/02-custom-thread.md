# Custom Thread

!!! secondary "creating custom thread"
    - We can inherit `Thread` class and create our own implementation of `run` method.
    - We only need to implement `__init__` and `run` method.
    - Then, we can use `start`, `join` and other methods as we did with `thread` class.

```python
from threading import Thread

class MyThread(Thread):
    def __init__(self, num):
        self.num = num
        super().__init__() # calling the parent class constructor (required)

    def run(self):
        for i in range(10):
            print(f"I'm thread: {self.num} => {i}")

if __name__ == "__main__":
    my_t = []
    for i in range(5):
        curr_t = MyThread(i+1)
        my_t.append(curr_t)

    print("=== start all the threads ===")
    for t in my_t:
        t.start()

    for t in my_t:
        t.join()

    print("=== all threads finished ===")
```

---

## Make custom daemon thread

- to make the thread `a daemon thread`, we can set `daemon=True` in the constructor.

```python
super().__init__(daemon=True)
```

---

## Methods of Thread

1. `start`: This method starts the thread.
2. `join(timeout=None)`: This method waits infinitely for the thread to finish.
3. `join(timeout)`: This method waits for the thread to finish for the specified time. `join()` method always return `None`. So to check if the `join() method` completed bcoz task is over, or due to timeout, we can use `is_alive()` method.

- If `is_alive()` returns `True`, then the thread is still running, and timeout has occurred (if `join(timeout)` is completed).
