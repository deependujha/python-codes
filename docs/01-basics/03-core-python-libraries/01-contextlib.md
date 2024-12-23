# Contextlib

- provides utilities for common tasks involving the `with statement`.

## What it provides?

!!! example ""
    - contextmanager
    - asynccontextmanager
    - closing
    - aclosing
    - nullcontext
    - suppress
    - redirect_stdout
    - redirect_stderr
    - chdir
    - ContextDecorator

---

## Implementing a simple Context Manager (using `class`)

- A class needs to implement `__enter__` and `__exit__` methods to be used as a context manager.

- `__enter__` method is called when the `with` block is entered. It doesn't take any arguments.
- `__exit__` method is called when the `with` block is exited. It takes three arguments:
    - `exc_type`: exception type
    - `exc_value`: exception value
    - `traceback`: traceback object
- If no exception occurs, all three arguments are `None`. Else, they contain the exception details.

```python
class MyCtx:
    def __init__(self, num):
        self.num = num

    def __enter__(self):
        print("enter block executing")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit block executing")


if __name__ == "__main__":
    with MyCtx(4) as c:
        print(f"value of {c.num=}")

    print("-"*40)
```

---

## `contextmanager` decorator

- A simpler way to create a context manager is to use the `contextmanager` decorator from the `contextlib` module.
- You don't need to implement a whole new class just to be able to use `with statements` with it.
- `function decorated with @contextmanager` should `yield` the resource that needs to be managed.
- Use try, except and finally blocks.
- `exception` raised inside the `with block` can be caught in the `except block`.
- `finally block` is used to clean up the resource, after the `with block` is exited.

```python
from contextlib import contextmanager

@contextmanager
def my_ctx(*args, **kwargs):
    try:
        print('Entering context')
        yield 'hello'
    except Exception as e:
        print(f'Caught exception: {e}')
    finally:
        print('Exiting context')

if __name__ == '__main__':
    with my_ctx() as val:
        print(f'Value: {val}')
    print("-"*50)
```

---

## AsyncContextManager

- similar to `contextmanager`, but for `async` functions.
- Used with `async with` statements.
- To implement, use `__aenter__` and `__aexit__` methods.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_connection():
    conn = await acquire_db_connection()
    try:
        yield conn
    finally:
        await release_db_connection(conn)

async def get_all_users():
    async with get_connection() as conn:
        return conn.query('SELECT ...')
```

---

## Closing

- closing is a helper function that simplifies the use of resources that need to be closed properly, such as files, sockets, or database connections.
- It ensures that the resource gets closed automatically when you're done with it, even if an error occurs.

!!! example "Why Use closing?"
    - Some objects don't support the with statement directly (they don't have a `__enter__` or `__exit__` method).
    - The closing function makes it possible to use these objects in a with block, ensuring proper cleanup.
    - When the block ends, closing calls the resource's `close() method` automatically

```python
from contextlib import contextmanager, closing

class MyCtx:
    def __init__(self, name):
        self.name = name
        print("myctx function called")
    def close(self):
        print("myctx close function called")


if __name__ == "__main__":
    with closing(MyCtx("deependu")) as m:
        print(m.name)
```

expected Output:

```txt
myctx function called
deependu
myctx close function called
```

---

## Aclosing

- `aclosing` is the async version of `closing`.

---

## NullContext

- `do-nothing` placeholder that can be used with `with statement`.
- Used when you don't need to do anything in the `__enter__` and `__exit__` methods.
- Mostly used for maintaining consistency in the code.
- Whatever a function returns, it should return support `with` statement.

```python
def myfunction(arg, ignore_exceptions=False):
    if ignore_exceptions:
        # Use suppress to ignore all exceptions.
        cm = contextlib.suppress(Exception)
    else:
        # Do not ignore any exceptions, cm has no effect.
        cm = contextlib.nullcontext()
    with cm:
        # Do something
```

- in the above code, we wanted to use `with block`, so we used `nullcontext` to maintain consistency.

---

## Suppress

- Return a context manager that suppresses any of the specified exceptions if they occur in the body of a with statement and then resumes execution with the first statement following the end of the with statement.

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove('somefile.tmp')

## equivalent to
# try:
#     os.remove('somefile.tmp')
# except FileNotFoundError:
#     pass
```

- To pass multiple exceptions, use a tuple.

```python
from contextlib import suppress

if __name__ == "__main__":
    with suppress((ValueError, FileNotFoundError)):
        raise ValueError()
        raise FileNotFoundError()
```

---

## Redirect_stdout

- Instead of printing to the console, you can redirect the output to a file or a string.
- To do this, we can modify the `sys.stdout` object to point to a different file or string.

```python
import sys

sys.stdout = open('output.txt', 'w')
print('This is redirected to a file')
```

- But, this is not a good practice, as it can lead to issues with other parts of the code that rely on `sys.stdout`, if we forget to reset it back to the original value.
- `redirect_stdout` provides a context manager that temporarily redirects `sys.stdout` to a different file or stream.

```python
from contextlib import redirect_stdout

with open('output.txt', 'w') as f:
    with redirect_stdout(f):
        print('This is redirected to a file')

print('This is printed to the console')
```

---

## Redirect_stderr

- Similar to `redirect_stdout`, but for `sys.stderr`.

---

## chdir

- This is a simple wrapper around chdir(), it `changes the current working directory upon entering and restores the old one on exit`.

---

## ContextDecorator

- Used to `create custom decorators` that can be `used as context managers`.
- `@contextmanager` is implemented using the same method.
- Class inheriting from `ContextDecorator` have to implement `__enter__` and `__exit__` as normal.

```python
from contextlib import ContextDecorator

class mycontext(ContextDecorator):
    def __enter__(self):
        print('Starting')
        return self

    def __exit__(self, *exc):
        print('Finishing')
        return False

# =============
@mycontext()
def function():
    print('The bit in the middle')

function()
# output:   Starting
#           The bit in the middle
#           Finishing

with mycontext():
    print('The bit in the middle')

# output:   Starting
#           The bit in the middle
#           Finishing
```

---

## How are they implemented?

### nullcontext

```python
class MyNullcontext:
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        pass
```

### closing

```python
class MyClosing:
    def __enter__(self, some_resource):
        return some_resource

    def __exit__(self, exc_type, exc_value, traceback):
        some_resource.close() # just calls the `close` method of the resource
```
