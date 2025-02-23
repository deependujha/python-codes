# Queues

!!! info
    - The queue module implements `multi-producer, multi-consumer` queues.
    - It is especially **`useful in threaded programming when information must be exchanged safely between multiple threads`**.

---

## Queue types

- `class queue.Queue(maxsize=0)`

> Constructor for a FIFO queue. maxsize is an integer that sets the upperbound limit on the number of items that can be placed in the queue. Insertion will block once this size has been reached, until queue items are consumed. If maxsize is less than or equal to zero, the queue size is infinite.

- `class queue.LifoQueue(maxsize=0)`

> Constructor for a LIFO queue. maxsize is an integer that sets the upperbound limit on the number of items that can be placed in the queue. Insertion will block once this size has been reached, until queue items are consumed. If maxsize is less than or equal to zero, the queue size is infinite.

- `class queue.PriorityQueue(maxsize=0)`

> Constructor for a priority queue. maxsize is an integer that sets the upperbound limit on the number of items that can be placed in the queue. Insertion will block once this size has been reached, until queue items are consumed. If maxsize is less than or equal to zero, the queue size is infinite.
>
> The lowest valued entries are retrieved first (the lowest valued entry is the one that would be returned by min(entries)). A typical pattern for entries is a tuple in the form: (priority_number, data).
>
> If the data elements are not comparable, the data can be wrapped in a class that ignores the data item and only compares the priority number:

---

## Queue methods

- `q.put(item[, block[, timeout]])`
- `q.get([block[, timeout]])`
- `q.qsize()`
- `q.empty()`
- `q.full()`
- `q.shutdown()` - signal the queue that no more items will be added
- `q.put_nowait(item)` (alias for `q.put(item, False)`) - don't block, if queue is empty, raise `exception: queue.Full`
- `q.get_nowait()` (alias for `q.get(False)`) - don't block, if queue is empty, raise `exception: queue.Empty`
- `q.join()` - block until all items in the queue are processed (queue is empty)

---

## Example

```python
import threading
import queue

q = queue.Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()

# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True).start()

# Send thirty task requests to the worker.
for item in range(30):
    q.put(item)

# Block until all tasks are done.
q.join()
print('All work completed')
```

---

## MultiProcessing Queue

- Queue from `import queue` is thread-safe, but not multiprocessing-safe.
- For multiprocessing, use `multiprocessing.Queue`

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

---

## DeQue

- `class collections.deque([iterable[, maxlen]])`
- `Deque` are thread-safe, but not multiprocessing-safe.

> Deque objects are like stacks or FIFO queues, as they support adding and removing elements from both ends.

- `deque.append(x)` - add x to the right side of the deque
- `deque.appendleft(x)` - add x to the left side of the deque
- `deque.pop()` - remove and return an element from the right side of the deque
- `deque.popleft()` - remove and return an element from the left side of the deque
- `deque.clear()` - remove all elements from the deque
- `deque.count(x)` - count the number of occurrences of x in the deque
- `deque.extend(iterable)` - extend the right side of the deque by appending elements from the iterable
- `deque.extendleft(iterable)` - extend the left side of the deque by appending elements from the iterable
- `deque.rotate(n)` - rotate the deque n steps to the right

```python
from collections import deque
d = deque('ghi')                 # make a new deque with three items
for elem in d:                   # iterate over the deque's elements
    print(elem.upper())

d.append('j')                    # add a new entry to the right side
d.appendleft('f')                # add a new entry to the left side
d                                # show the representation of the deque

d.pop()                          # return and remove the rightmost item

d.popleft()                      # return and remove the leftmost item

list(d)                          # list the contents of the deque

d[0]                             # peek at leftmost item

d[-1]                            # peek at rightmost item

list(reversed(d))                # list the contents of a deque in reverse

'h' in d                         # search the deque

d.extend('jkl')                  # add multiple elements at once
d

d.rotate(1)                      # right rotation
d

d.rotate(-1)                     # left rotation
d

deque(reversed(d))               # make a new deque in reverse order

d.clear()                        # empty the deque
d.pop()                          # cannot pop from an empty deque

d.extendleft('abc')              # extendleft() reverses the input order
d
```
