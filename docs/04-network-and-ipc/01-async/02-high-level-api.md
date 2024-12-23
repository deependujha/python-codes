# High-Level APIs of `asyncio`

`asyncio` is Python's library for asynchronous programming, allowing you to run tasks concurrently without using threads or processes.

---

## Key Concepts

### **1. Coroutine**

- A function defined using `async def`.
- Can be paused and resumed using `await`.
- Example:

  ```python
  async def my_coroutine():
      await asyncio.sleep(1)  # Pause for 1 second
      print("Done!")
  ```

### **2. Event Loop**

- Manages the execution of coroutines and tasks.
- High-level APIs automatically handle the event loop for you.

### **3. Task**

- A coroutine wrapped in a `Task` object, which runs concurrently.
- Created using `asyncio.create_task()`.

---

## High-Level Functions

### **1. `asyncio.run(coro)`**

- Runs the given coroutine and closes the event loop after completion.
- Use it as the entry point for your asynchronous program.
- Example:

  ```python
  async def main():
      print("Hello, asyncio!")

  asyncio.run(main())
  ```

### **2. `asyncio.gather(*coros)`**

- Runs multiple coroutines concurrently and collects their results.
- Results are returned in the same order as the coroutines were passed.
- Example:

  ```python
  async def task(name, delay):
      await asyncio.sleep(delay)
      return f"Task {name} done"

  async def main():
      results = await asyncio.gather(task("A", 2), task("B", 1))
      print(results)  # Output: ['Task A done', 'Task B done']

  asyncio.run(main())
  ```

### **3. `asyncio.create_task(coro)`**

- Starts a coroutine as a background task and returns a `Task` object.
- The task runs concurrently with other coroutines.
- Example:

  ```python
  async def task(name, delay):
      await asyncio.sleep(delay)
      print(f"{name} finished")

  async def main():
      t1 = asyncio.create_task(task("Task 1", 2))
      t2 = asyncio.create_task(task("Task 2", 1))
      await t1
      await t2

  asyncio.run(main())
  ```

### **4. `await asyncio.sleep(seconds)`**

- Asynchronously pauses execution for the given number of seconds.
- Allows other tasks to run during the pause.
- Example:

  ```python
  async def main():
      print("Start")
      await asyncio.sleep(1)
      print("End after 1 second")

  asyncio.run(main())
  ```

---

## Error Handling

### **Catching Exceptions in `gather`**

- Use `try/except` around `asyncio.gather()` to catch exceptions from any coroutine.
- Example:

  ```python
  async def faulty_task():
      raise ValueError("Something went wrong")

  async def main():
      try:
          await asyncio.gather(faulty_task())
      except Exception as e:
          print(f"Caught exception: {e}")

  asyncio.run(main())
  ```

### **`return_exceptions=True` in `gather`**

- Collect exceptions without canceling other tasks.
- Example:

  ```python
  async def faulty_task():
      raise ValueError("Something went wrong")

  async def main():
      results = await asyncio.gather(
          faulty_task(),
          asyncio.sleep(1),
          return_exceptions=True
      )
      print(results)  # Output: [ValueError('Something went wrong'), None]

  asyncio.run(main())
  ```

---

## Common Patterns

### **Run Coroutines Concurrently**

Use `gather` or `create_task` for concurrency:

```python
async def task1():
    await asyncio.sleep(2)
    print("Task 1 done")

async def task2():
    await asyncio.sleep(1)
    print("Task 2 done")

async def main():
    await asyncio.gather(task1(), task2())  # Runs both tasks concurrently

asyncio.run(main())
```

---

### **Cancel a Task**

```python
async def main():
    task = asyncio.create_task(asyncio.sleep(10))
    await asyncio.sleep(1)
    task.cancel()  # Cancels the task
    try:
        await task
    except asyncio.CancelledError:
        print("Task was cancelled!")

asyncio.run(main())
```

---

## Summary

1. Use `async def` and `await` to define and run coroutines.
2. Use `asyncio.run` to execute your main coroutine.
3. Use `asyncio.gather` or `create_task` for concurrency.
4. Handle errors with `try/except` or `return_exceptions=True`.
