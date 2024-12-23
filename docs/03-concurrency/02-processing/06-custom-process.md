# Custom Process

## **Why Create a Custom Process?**

- Subclassing `multiprocessing.Process` is useful when you need to **encapsulate specific data or behavior for each process**. (Like LitData DataWorker, a process class that downloads data, processes it, and saves it to a database.)
- Allows defining a custom `run()` method, which will be executed when the process starts.

---

## Implementation 🤓

!!! secondary "creating custom process"
    - Very similar to `creating custom thread`.
    - We can inherit `Process` class and create our own implementation of `run` method.
    - We only need to implement `__init__` and `run` method.
    - Then, we can use `start`, `join` and other methods as we did with `Process` class.

```python
from multiprocessing import Process

class MyProcess(Process):
    def __init__(self, num):
        self.num = num
        super().__init__() # calling the parent class constructor (required)

    def run(self):
        for i in range(10):
            print(f"I'm process: {self.num} => {i}")

if __name__ == "__main__":
    my_p = []
    for i in range(5):
        curr_p = MyProcess(i+1)
        my_p.append(curr_p)

    print("=== start all the processes ===")
    for p in my_p:
        p.start()

    for p in my_p:
        p.join()

    print("=== all processes finished ===")
```
