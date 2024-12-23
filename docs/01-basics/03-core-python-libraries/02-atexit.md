# AtExit (`atexit`) Module

The **`atexit`** module in Python allows you to register functions that will run automatically when the program is about to exit.

- This is useful for performing cleanup tasks like closing files, releasing resources, or printing goodbye messages.

---

## Basic Usage of `atexit`

- **Registering Functions**:
    Use `atexit.register(function_name)` to register a function that will be called upon program termination.

- **Automatic Execution**:
    Registered functions are executed in the reverse order of their registration when the program exits normally (no crashes or `os._exit`).

- **Unregistering Functions**:
    You can unregister a function using `atexit.unregister(function_name)`.

---

## Registering a Function

```python
import atexit

def goodbye():
    print("Program is exiting... Goodbye!")

# Register the function
atexit.register(goodbye)

# Program logic
print("Hello, World!")
```

**Output:**

```txt
Hello, World!
Program is exiting... Goodbye!
```

---

## Multiple Registered Functions

```python
import atexit

def func1():
    print("First cleanup function.")

def func2():
    print("Second cleanup function.")

# Register both functions
atexit.register(func1)
atexit.register(func2)

print("Program is running...")
```

**Output:**

```txt
Program is running...
Second cleanup function.
First cleanup function.
```

*Note:* Functions are called in reverse order of their registration (`func2` runs before `func1`).

---

## Passing Arguments to Functions

You can use `atexit.register` with additional arguments:

```python
import atexit

def greet(name):
    print(f"Goodbye, {name}!")

# Register with arguments
atexit.register(greet, "Alice")

print("Program is running...")
```

**Output:**

```txt
Program is running...
Goodbye, Alice!
```

---

## Using `lambda` Functions

You can register anonymous functions with `lambda`:

```python
import atexit

atexit.register(lambda: print("Lambda function executed!"))

print("Program is running...")
```

**Output:**

```txt
Program is running...
Lambda function executed!
```

---

## `atexit` decorator

```python
import atexit

@atexit.register
def goodbye():
    print('You are now leaving the Python sector.')
```

---

## Key Points to Remember

1. **Normal Exit Only**: Functions registered with `atexit` are executed only during a normal exit (not if the program crashes or `os._exit()` is called).

2. **Reverse Execution**: Functions are executed in reverse order of their registration.

3. **Use Cases**: Cleanup tasks, logging program termination, closing open resources.

---

## Summary

!!! quote ""
    - The `atexit` module is a handy way to manage cleanup tasks when your program exits.
    - By registering functions with `atexit.register`, you ensure they run automatically at termination.
    - It’s particularly useful for tasks like saving state, closing connections, or releasing resources.
