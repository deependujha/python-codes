# Pytest Basic Usage

## Assert that something is true

```python
# content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5 # pytest should fail
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
