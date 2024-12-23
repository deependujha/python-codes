# Communication in Multiprocessing

- Processes can push values to a queue and pull values from a **queue**(`most important`).
- Two processes can communicate with each other using a pipe.
- Processes can **share memory** using shared memory objects. If one process changes the value, the other process can see the change.

---

## Shared Memory

### `Value`

- `Value` is a shared memory object that allows you to store a single value.
- Specify the type of the value and the initial value.
- Read and write the value using the `value` attribute.

### `Array`

- `Array` is a shared memory object that allows you to store a sequence of values.
- Specify the type of the value and the length.

```python
from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
```

---

## Queue

- `Queue` is a thread and process-safe queue.
- It allows multiple processes to push and pull values from the queue.

```python
from multiprocessing import Process, Queue

def f(q):
    q.put([42, None, 'hello'])

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()
```

!!! info "methods of Queue"
    - `put(obj, block=True, timeout=None)`: Push a value to the queue. If queue is full, block and wait until the queue doesn't have any space, then push. If timeout is not None, it will wait for the specified time, and then raise `queue.Full` exception if the queue is still full.
    - `put_nowait(obj)`: Push a value to the queue. If the queue is full, raise `queue.Full` exception.
    - `get(block=True, timeout=None)`: Pull a value from the queue. If no value is available, block and wait until a value is available. If timeout is not None, it will wait for the specified time, and then raise `queue.Empty` exception if the queue is still empty.
    - `get_nowait()`: Pull a value from the queue. If no value is available, raise `queue.Empty` exception.
    - `empty()`: Return `True` if the queue is empty.
    - `full()`: Return `True` if the queue is full.
    - `qsize()`: Return the number of items in the queue.
    - `close()`: Close the queue.
    - `join_thread()`: Join the background thread. This can only be used after close() has been called. It blocks until the background thread exits, ensuring that all data in the buffer has been flushed to the pipe.

---

## Pipe

- `Pipe` is a two-way communication channel between two processes.
- It returns two connection objects that represent the two ends of the pipe.
- Both connection objects have `send()` and `recv()` methods.
- data in a pipe may become corrupted if two processes (or threads) try to read from or write to the same end of the pipe at the same time.
- Of course there is no risk of corruption from processes using different ends of the pipe at the same time.

```python
from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()
```

- Each connection object (`parent_conn` & `child_conn`) returned by pipe have multiple ways to transfer data.

!!! info "connection object methods"
    - `send()`: Send data to the other end of the pipe.
    - `recv()`: Receive data from the other end of the pipe.
    - `poll(timeout=None)`: Return `True` if there is any data to read.
    - `send_bytes(buffer)`: Send a bytes object.
    - `recv_bytes(maxlength)`: Receive a bytes object.
    - `recv_bytes_into(buffer)`: Receive a bytes object into a buffer.

```ipython
>>> from multiprocessing import Pipe
>>>
>>> a, b = Pipe()
>>>
>>> a.send([1, 'hello', None])
>>> b.recv()
[1, 'hello', None]
>>>
>>> b.send_bytes(b'thank you')
>>> a.recv_bytes()
b'thank you'
>>>
>>> import array
>>>
>>> arr1 = array.array('i', range(5))
>>> arr2 = array.array('i', [0] * 10)
>>>
>>> a.send_bytes(arr1)
>>> count = b.recv_bytes_into(arr2)
>>> assert count == len(arr1) * arr1.itemsize
>>> arr2
array('i', [0, 1, 2, 3, 4, 0, 0, 0, 0, 0])
```
