# Concurrency with Queus

```python
from concurrent.futures import ThreadPoolExecutor
import time
import threading
from queue import Queue


def task(n: int, q: Queue):
    print(f"{n} Task assigned to thread: {threading.current_thread().name}")
    time.sleep(n)
    q.put_nowait(n)
    return n * n


def process_thread(q: Queue, rm_q: Queue):
    while True:
        item = q.get()
        if item is None:  # Sentinel value to exit
            break
        print(f"processing {item} in thread")
        rm_q.put_nowait(item)


def delete_thread(q: Queue):
    while True:
        item = q.get()
        if item is None:  # Sentinel value to exit
            break
        print(f"removing {item} in thread")


def worker(inputs, num_workers):
    ready_to_process_queue = Queue()
    ready_to_delete_queue = Queue()

    t1 = threading.Thread(
        target=process_thread,
        name="t1",
        args=(ready_to_process_queue, ready_to_delete_queue),
    )
    t2 = threading.Thread(
        target=delete_thread, name="t2", args=(ready_to_delete_queue,)
    )

    t1.start()
    t2.start()

    print("going to start thread pool executor")

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for n in inputs:
            executor.submit(task, n, ready_to_process_queue)
    print("all task submitted to thread")
    ready_to_process_queue.put_nowait(None)
    print("pushed None to process queue. going to wait for it finish now")
    t1.join()
    # Stop delete_thread **after** processing is complete
    ready_to_delete_queue.put_nowait(None)
    t2.join()


if __name__ == "__main__":
    inputs = [3, 1, 4, 5, 2]
    worker(inputs, 3)
```
