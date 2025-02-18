# Semaphores

## **Scenario**  

Imagine **3 workers** trying to access a **shared resource**, but only **2 workers** can access it at a time. A semaphore ensures that no more than 2 workers use the resource simultaneously.

---

## **Multithrading semaphore**

```python
import threading
import time

# Create a semaphore with a max of 2 concurrent accesses
semaphore = threading.Semaphore(2)

def worker(worker_id):
    print(f"Worker {worker_id} is waiting to access the resource...")
    with semaphore:  # Acquire the semaphore (decrements count)
        print(f"Worker {worker_id} acquired access! 🚀")
        time.sleep(2)  # Simulating work
        print(f"Worker {worker_id} released access! ✅")

# Create 3 worker threads
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print("All workers finished execution!")
```

---

## **How It Works**

1. **Semaphore(2)** → At most **2 workers** can enter the critical section at a time.
2. **Each worker waits** until the semaphore allows it to proceed.
3. **Once inside, the worker "locks" the resource**, works for 2 seconds, then releases it.
4. **New workers enter when a previous worker exits**.

---

## **Expected Output**

```plaintext
Worker 0 is waiting to access the resource...
Worker 1 is waiting to access the resource...
Worker 0 acquired access! 🚀
Worker 1 acquired access! 🚀
Worker 2 is waiting to access the resource...
Worker 0 released access! ✅
Worker 2 acquired access! 🚀
Worker 1 released access! ✅
Worker 2 released access! ✅
All workers finished execution!
```

- Workers **0 and 1** get access first.
- Worker **2 waits** until one of them finishes.
- When **Worker 0 or 1 releases**, **Worker 2 gets access**.

---

## **Why Use This?**

- Prevents **too many threads** from overwhelming a resource.
- Useful for **limiting concurrent database access, API calls, GPU processing, etc.**
- Essential in **multiprocessing** (like PyTorch `DataLoader`) to prevent **semaphore leaks**.

---

!!! info
    Just like **threading.Semaphore**, we have **semaphores** for both **multiprocessing** and **async (asyncio)**.

---

## **1️⃣ Multiprocessing Semaphore**

- Used to control **processes** accessing a shared resource.
- Works like `threading.Semaphore`, but for multiple processes instead of threads.

### **Example multiprocessing-semaphore**

```python
import multiprocessing
import time

# Create a multiprocessing semaphore (max 2 processes can access at a time)
semaphore = multiprocessing.Semaphore(2)

def worker(worker_id):
    print(f"Process {worker_id} waiting to access the resource...")
    with semaphore:  # Acquire the semaphore
        print(f"Process {worker_id} acquired access! 🚀")
        time.sleep(2)  # Simulate work
        print(f"Process {worker_id} released access! ✅")

# Create 3 processes
processes = []
for i in range(3):
    p = multiprocessing.Process(target=worker, args=(i,))
    processes.append(p)
    p.start()

# Wait for all processes to finish
for p in processes:
    p.join()

print("All processes finished execution!")
```

### **Expected Behavior**

- At most **2 processes** can access the critical section at the same time.
- Other processes **wait** until a slot is freed.

---

## **2️⃣ Asyncio Semaphore**

- Used to **limit concurrency in async tasks**.
- Unlike threading/multiprocessing, it **does not block** but **awaits** when access is unavailable.

### **Example asyncio-semaphore**

```python
import asyncio

# Create an asyncio semaphore (max 2 tasks can access at a time)
semaphore = asyncio.Semaphore(2)

async def worker(worker_id):
    print(f"Task {worker_id} waiting to access the resource...")
    async with semaphore:  # Acquire semaphore asynchronously
        print(f"Task {worker_id} acquired access! 🚀")
        await asyncio.sleep(2)  # Simulating work
        print(f"Task {worker_id} released access! ✅")

async def main():
    tasks = [worker(i) for i in range(3)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

### **Expected**

- **Two tasks run at the same time**.
- The **third task waits** until one of them releases the semaphore.

---

## **🚀 When to Use What?**

| **Scenario**           | **Use**                  |
|------------------------|-------------------------|
| Multi-threading        | `threading.Semaphore()` |
| Multi-processing       | `multiprocessing.Semaphore()` |
| Async I/O operations   | `asyncio.Semaphore()` |
