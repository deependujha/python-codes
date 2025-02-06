# Fixtures

A **fixture** in testing is just **preparation code** that sets up everything needed before a test runs (e.g., creating a test database, initializing objects, or setting configurations).  

!!! info ""
    We call it a **fixture** because it **fixes** or **sets up** a stable environment for tests, ensuring they always start with the same conditions.

- A function marked with `@pytest.fixture`, is a fixture.
- `test functions` request `fixtures` they require by **declaring them as arguments**.

!!! success "**`conftest.py`** file"
    conftest.py is a special pytest configuration file that provides shared fixtures and hooks for tests without needing explicit imports.

```python
@pytest.fixture
def my_num():
    return 2

def test_num(my_num):
    assert my_num == 2
```

---

## Fixtures can request other fixtures

```python
# contents of test_append.py
import pytest


# Arrange
@pytest.fixture
def first_entry():
    return "a"


# Arrange
@pytest.fixture
def order(first_entry):
    return [first_entry]


def test_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]


def test_int(order):
    # Act
    order.append(2)

    # Assert
    assert order == ["a", 2]
```

---

## Autouse fixtures (fixtures you don’t have to request)

- Sometimes you may want to have a fixture (or **`even several`**) that you know all your tests will depend on.

```python
import pytest


@pytest.fixture
def first_entry():
    return "a"


@pytest.fixture
def order(first_entry):
    return []


@pytest.fixture(autouse=True)
def append_first(order, first_entry):
    return order.append(first_entry)


def test_string_only(order, first_entry):
    assert order == [first_entry]


def test_string_and_int(order, first_entry):
    order.append(2)
    assert order == [first_entry, 2]
```

---

## Teardown/cleanup (fixture finalization)

- In fixture, rather than `return`, use `yield`, after yielding, write cleanup code.

```python
# from lightning-ai/litdata/tests/conftest.py file

@pytest.fixture(autouse=True)
def teardown_process_group():
    """Ensures distributed process group gets closed before the next test runs."""
    yield
    if torch.distributed.is_available() and torch.distributed.is_initialized():
        torch.distributed.destroy_process_group()
```

!!! info "Fixture setup & teardown"
    Think of fixture function to be split in two parts. `setup | yield | teardown`

    ```python
    @pytest.fixture
    def my_fixt():
        print("this is my setup code")
        yield {"name":"deep"} # or whatever you wish to return
        print("this is my teardown code")
    ```

---

## Scope of fixtures

- Fixtures requiring network access depend on connectivity and are usually time-expensive to create.
- We can add a `scope="module"` parameter to the `@pytest.fixture` invocation to cause a fixture function, so it will only be invoked once per test module (the default is to invoke once per test function).
- Multiple test functions in a test module will thus each receive the same fixture instance, thus saving time.

| **Scope**    | detail |
| -------- | ------- |
| function (**default**)  | the fixture is destroyed at the end of the test.    |
| class | the fixture is destroyed during teardown of the last test in the class.    |
| module    | the fixture is destroyed during teardown of the last test in the module.    |
| package    | the fixture is destroyed during teardown of the last test in the package where the fixture is defined, including sub-packages and sub-directories within it.    |
| session    | the fixture is destroyed at the end of the test session.    |

```python
@pytest.fixture(scope="session")
def smtp_connection():
    # the returned fixture value will be shared for
    # all tests requesting it
    ...
```
