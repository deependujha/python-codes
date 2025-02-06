# Pytest Basic Usage

## Assert that something is true

```python
# content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5, "some msgto be printed in the traceback if fails"
```

---

## Assert that a certain exception is raised

```python
# content of test_sysexit.py
import pytest


def f():
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        f()
```

---

## Matching `Exception` messages

```python
import pytest


def myfunc():
    raise ValueError("Exception 123 raised")


def test_match():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        myfunc()
```

---

## Using `context` provided by `raises`

```python
def test_foo_not_implemented():
    def foo():
        raise NotImplementedError

    with pytest.raises(RuntimeError) as excinfo:
        foo()
    assert excinfo.type is RuntimeError
```

---

## Handling `ExceptionGroup` in pytest

- You can also use the context provided by raises to assert that an expected exception is part of a raised `ExceptionGroup`:

```python
# content of test_exceptiongroup.py
import pytest


def f():
    raise ExceptionGroup(
        "Group message",
        [
            RuntimeError(),
        ],
    )


def test_exception_in_group():
    with pytest.raises(ExceptionGroup) as excinfo:
        f()
    assert excinfo.group_contains(RuntimeError)
    assert not excinfo.group_contains(TypeError)
```

---

## Group multiple tests in a class

- Class name should be prefixed with `Test`, and method names should be prefixed with `test`.
- No `__init__` method should be there.

```python
# content of test_class_demo.py
class TestClassDemoInstance:
    value = 0

    def test_one(self):
        self.value = 1
        assert self.value == 1

    def test_two(self):
        assert self.value == 1 # will fail, as each test run has unique instance
```

!!! bug "Grouping tests in class"
    Inside classes, `each test has a unique instance of the class`.

---

## `xfail mark` and `pytest.raises`

```python
def f():
    raise IndexError()


@pytest.mark.xfail(raises=IndexError)
def test_f():
    f()
```

- This will only “xfail” if the test fails by raising IndexError or subclasses.

!!! warning "`xfail` v/s `raises` So when to use which one?"
    - If there's an existing bug that is yet to be fixed, use `xfail`. It will help you in documenting unfixed bugs when you decide to fix.
    - `pytest.raises` is likely to be better for cases where you are testing exceptions your own code is deliberately raising, which is the majority of cases.
