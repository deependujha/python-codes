# Low-Level Overview of `asyncio`

The low-level APIs in `asyncio` provide finer control over the event loop, tasks, and protocols. These are useful for advanced use cases like integrating `asyncio` with custom frameworks or building servers.

---

## Key Low-Level APIs

### **1. Event Loop**

- The event loop manages the execution of asynchronous tasks and handles I/O.
- Use `asyncio.get_event_loop()` or `asyncio.new_event_loop()` to work with it.
- Example:

  ```python
  import asyncio

  async def main():
      print("Running in the event loop")

  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())  # Manually run the coroutine
  loop.close()  # Always close the loop when done
  ```

---

### **2. Future**

- A placeholder for a result that hasn’t been computed yet.
- Usually created internally by `asyncio`, but you can use it manually.
- Example:

  ```python
  import asyncio

  loop = asyncio.get_event_loop()
  future = loop.create_future()

  # Set the result of the future
  loop.call_soon(future.set_result, "Result is ready")

  # Get the result
  print(loop.run_until_complete(future))  # Output: "Result is ready"
  ```

---

### **3. Task**

- A `Task` is a coroutine that is being executed by the event loop.
- You can use `asyncio.create_task()` (high-level) or `loop.create_task()` (low-level) to create tasks.
- Example:

  ```python
  import asyncio

  async def say_hello():
      await asyncio.sleep(1)
      print("Hello!")

  loop = asyncio.get_event_loop()
  task = loop.create_task(say_hello())  # Manually create a task
  loop.run_until_complete(task)
  loop.close()
  ```

---

### **4. Custom Event Loop**

- You can create and manage a custom event loop for advanced use cases.
- Example:

  ```python
  import asyncio

  async def my_task():
      await asyncio.sleep(1)
      print("Task completed!")

  # Create a new event loop
  custom_loop = asyncio.new_event_loop()
  asyncio.set_event_loop(custom_loop)

  custom_loop.run_until_complete(my_task())
  custom_loop.close()
  ```

---

## Low-Level Tasks Management

### **1. `loop.call_soon()`**

- Schedules a callback to be executed as soon as possible.
- Example:

  ```python
  import asyncio

  def my_callback():
      print("Callback executed!")

  loop = asyncio.get_event_loop()
  loop.call_soon(my_callback)
  loop.run_forever()  # Will execute the callback and then keep running
  ```

### **2. `loop.call_later()`**

- Schedules a callback to be executed after a specific delay.
- Example:

  ```python
  import asyncio

  def delayed_callback():
      print("Callback executed after delay!")

  loop = asyncio.get_event_loop()
  loop.call_later(2, delayed_callback)  # 2-second delay
  loop.run_forever()
  ```

---

## Custom Futures and Tasks

### **1. Using `asyncio.Future`**

- Create your own placeholder for asynchronous results.
- Example:

  ```python
  import asyncio

  def set_future_result(future):
      future.set_result("Future is done!")

  loop = asyncio.get_event_loop()
  future = asyncio.Future()

  loop.call_soon(set_future_result, future)
  print(loop.run_until_complete(future))  # Output: "Future is done!"
  ```

### **2. Running Coroutines as Tasks**

- Coroutines need to be wrapped in a `Task` for the event loop to execute them.
- Example:

  ```python
  import asyncio

  async def my_task():
      print("Task running...")
      await asyncio.sleep(1)
      print("Task finished!")

  loop = asyncio.get_event_loop()
  task = asyncio.ensure_future(my_task())  # Wrap coroutine in a Task
  loop.run_until_complete(task)
  ```

---

## Usage

```python
async def set_after(fut, delay, value):
    # Sleep for *delay* seconds.
    await asyncio.sleep(delay)

    # Set *value* as a result of *fut* Future.
    fut.set_result(value)

async def main():
    # Get the current event loop.
    loop = asyncio.get_running_loop()

    # Create a new Future object.
    fut = loop.create_future()

    # Run "set_after()" coroutine in a parallel Task.
    # We are using the low-level "loop.create_task()" API here because
    # we already have a reference to the event loop at hand.
    # Otherwise we could have just used "asyncio.create_task()".
    loop.create_task(
        set_after(fut, 1, '... world'))

    print('hello ...')

    # Wait until *fut* has a result (1 second) and print it.
    print(await fut)

asyncio.run(main())
```

---

## Error Handling in Low-Level APIs

### **Handle Task Exceptions**

- Example:

  ```python
  import asyncio

  async def faulty_task():
      raise ValueError("Oops!")

  loop = asyncio.get_event_loop()
  task = loop.create_task(faulty_task())

  try:
      loop.run_until_complete(task)
  except ValueError as e:
      print(f"Caught exception: {e}")
  ```

---

## Summary

- Low-level APIs are for fine-grained control, like managing custom event loops or working with protocols and transports.
- Use **Futures** to represent pending results, and **Tasks** to run coroutines concurrently.
- Low-level APIs are generally for advanced use cases; stick to high-level APIs for most tasks.
