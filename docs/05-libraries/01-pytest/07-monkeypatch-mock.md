# Monkeypatch & Mocking

!!! bug "What does **Monkeypatch** even mean?"
    - Modifying properties/methods at **runtime** without changing the actual code logic.

    ```python
    from SomeOtherProduct.SomeModule import SomeClass

    def speak(self):
        return "ook ook eee eee eee!"

    SomeClass.speak = speak
    ```

- Sometimes tests need to invoke functionality which depends on global settings or which invokes code which cannot be easily tested such as network access.
- The monkeypatch fixture helps you to safely set/delete an attribute, dictionary item or environment variable, or to modify sys.path for importing.

---

## **`monkeypatch`** fixture

!!! example "monkeypatch fixture"
    > Modifying the behavior of a **function** or the **property of a class** for a test

    - **monkeypatch.setattr(obj, name, value, raising=True)**
    - **monkeypatch.delattr(obj, name, raising=True)**

    ---

    > Modifying the values of **dictionaries**

    - **monkeypatch.setitem(mapping, name, value)**
    - **monkeypatch.delitem(obj, name, raising=True)**

    ---

    > Modifying **env variables**. 
    >
    > With `prepend = "some_val"`, the env-var won't be overwritten, but just `value+prepend_str+old_env_value`
    >
    > With `prepend=None`, it simply replaces the old env value with new value. 

    - **monkeypatch.setenv(name, value, prepend=None)**
    - **monkeypatch.delenv(name, raising=True)**

    ---

    - **monkeypatch.syspath_prepend(path)**
    - **monkeypatch.chdir(path)**
    - **monkeypatch.context()**

- **`All modifications will be undone after the requesting test function or fixture has finished`**.
- The `raising` parameter determines if a `KeyError` or `AttributeError` will be raised if the target of the set/deletion operation does not exist.

```python
import pytest

class MyClass:
    value = 42

def test_patch(monkeypatch):
    monkeypatch.setattr(MyClass, "value", 100)  # Works fine
    monkeypatch.setattr(MyClass, "non_existent", 200, raising=False)  # No error
    # monkeypatch.setattr(MyClass, "non_existent", 200, raising=True)  # Raises AttributeError
```

- If `raising=True (default)`, pytest will raise an error if the attribute does not already exist in the target object.

---

## Monkeypatch `functions`

```python
# contents of test_module.py with source code and the test
from pathlib import Path


def getssh():
    """Simple function to return expanded homedir ssh path."""
    return Path.home() / ".ssh"


def test_getssh(monkeypatch):
    # mocked return function to replace Path.home
    # always return '/abc'
    def mockreturn():
        return Path("/abc")

    # Application of the monkeypatch to replace Path.home
    # with the behavior of mockreturn defined above.
    monkeypatch.setattr(Path, "home", mockreturn)

    # Calling getssh() will use mockreturn in place of Path.home
    # for this test with the monkeypatch.
    x = getssh()
    assert x == Path("/abc/.ssh")
```

---

## Monkeypatch **`returned objects`**

```python
# contents of test_app.py, a simple test for our API retrieval
# import requests for the purposes of monkeypatching
import requests

# our app.py that includes the get_json() function
# this is the previous code block example
import app


# custom class to be the mock return value
# will override the requests.Response returned from requests.get
class MockResponse:
    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


def test_get_json(monkeypatch):
    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockResponse()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    # app.get_json, which contains requests.get, uses the monkeypatch
    result = app.get_json("https://fakeurl")
    assert result["mock_key"] == "mock_response"
```

---

## Monkeypatch `context`

```python
import functools


def test_partial(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(functools, "partial", 3)
        assert functools.partial == 3
```

---

## Monkeypatch `dictionaries`

```python
# contents of app.py to generate a simple connection string
DEFAULT_CONFIG = {"user": "user1", "database": "db1"}


def create_connection_string(config=None):
    """Creates a connection string from input or defaults."""
    config = config or DEFAULT_CONFIG
    return f"User Id={config['user']}; Location={config['database']};"

# ============================

# contents of test_app.py
# app.py with the connection string function (prior code block)
import app


def test_connection(monkeypatch):
    # Patch the values of DEFAULT_CONFIG to specific
    # testing values only for this test.
    monkeypatch.setitem(app.DEFAULT_CONFIG, "user", "test_user")
    monkeypatch.setitem(app.DEFAULT_CONFIG, "database", "test_db")

    # expected result based on the mocks
    expected = "User Id=test_user; Location=test_db;"

    # the test uses the monkeypatched dictionary settings
    result = app.create_connection_string()
    assert result == expected

def test_missing_user(monkeypatch):
    # patch the DEFAULT_CONFIG t be missing the 'user' key
    monkeypatch.delitem(app.DEFAULT_CONFIG, "user", raising=False)

    # Key error expected because a config is not passed, and the
    # default is now missing the 'user' entry.
    with pytest.raises(KeyError):
        _ = app.create_connection_string()
```

---

## Monkeypatch `env variables`

```python
# contents of our original code file e.g. code.py
import os


def get_os_user_lower():
    """Simple retrieval function.
    Returns lowercase USER or raises OSError."""
    username = os.getenv("USER")

    if username is None:
        raise OSError("USER environment is not set.")

    return username.lower()

# ========================

# contents of our test file e.g. test_code.py
import pytest


def test_upper_to_lower(monkeypatch):
    """Set the USER env var to assert the behavior."""
    monkeypatch.setenv("USER", "TestingUser")
    assert get_os_user_lower() == "testinguser"


def test_raise_exception(monkeypatch):
    """Remove the USER env var and assert OSError is raised."""
    monkeypatch.delenv("USER", raising=False)

    with pytest.raises(OSError):
        _ = get_os_user_lower()
```

---

## Monkeypatch as `fixtures`

- Using monkeypatch code in fixtures fixes the hassle to write it everytime you need it.

```python
import pytest
import os

# A simple test where we patch the environment variable
@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("MY_VAR", "fake_value")

def test_env_var(mock_env):
    assert os.getenv("MY_VAR") == "fake_value"
```

- By default, **`fixtures have a function scope`**, meaning they are created and destroyed for each test.
- You can adjust the scope if you want them to persist across multiple tests (e.g., using `scope="module"`).

For details: [check here](./03-fixtures.md#scope-of-fixtures)
