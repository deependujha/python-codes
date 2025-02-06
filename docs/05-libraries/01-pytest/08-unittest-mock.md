# unittest.mock

- The unittest library is part of the `standard library` but is often used together with pytest.
- `unittest.mock` provides us with 3 most often used class and decorator.
- `Mock`, `MagicMock` and `@patch`.

---

## `Mock`

- `Mock` are `callable` and `create attributes as new mocks when you access them`.
- Mocks record how you use them, allowing you to make assertions about what your code has done to them.
- We can **check** if, `mock was called`, was `called only once`, was `called with some args`, was `never called`, etc.

- Refer [here](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock) for the whole list.

```python
from unittest.mock import Mock

m = Mock()

m()

m.assert_called()
m.assert_called_once()

m(1, 2, 3, test='wow')
m.assert_called_with(1, 2, 3, test='wow')

m('foo', bar='baz')
m.assert_called_once_with('other', bar='values')

m(1, 2, arg='thing')
m.assert_any_call(1, 2, arg='thing')
```

- On mock object, we can call arbitrary method.

```python
from unittest.mock import Mock

m = Mock()
m.meow()
m.meow.bhow()
```

!!! info "Default Mock return value: `sentinel.DEFAULT`"
    When you call a mock object, it returns a DEFAULT which is `sentinel.DEFAULT`. It can be used by side_effect functions to indicate that the normal return value should be used.

- But, we can also specify a **`fixed return value`**.

```python
from unittest.mock import Mock

m = Mock(return_value=5)

for _ in range(50):
    m() # 5
```

- Mock object have a **side_effect** property, which if is a `function, is called everytime the mock object is called`.

```python
from unittest.mock import Mock

def some_fn(self):
    return 5

m = Mock()

m() # senitnel.DEFAULT

m.side_effect = some_fn

m() # 5
```

- We can also specify it in constructor.

```python
m = Mock(side_effect = some_fn)
```

- If `side_effect` is a list/iterable, each function call returns the first element from the list, and removes it. When all elements are exhausted, it throws `StopIteration` error on further calling.

```python
from unittest.mock import Mock

m = Mock(side_effect = [5,4,3,2,1])

for _ in range(6):
    print(m()) # [5,4,3,2,1, StopIteration error]
```

!!! note
    `side_effect` takes precedence over `return_value`.

---

## MagicMock

- `MagicMock` is a superset (derived class) of Mock class. It has all the features as `Mock` class has, but also implements many `magic methods`, like:

```txt
__hash__, __sizeof__, __repr__ and __str__

__round__, __floor__, __trunc__ and __ceil__

Comparisons: __lt__, __gt__, __le__, __ge__, __eq__ and __ne__

Container methods: __getitem__, __setitem__, __delitem__, __contains__, __len__, __iter__, __reversed__ and __missing__

Context manager: __enter__, __exit__, __aenter__ and __aexit__

Unary numeric methods: __neg__, __pos__ and __invert__

The numeric methods (including right hand and in-place variants): __add__, __sub__, __mul__, __matmul__, __truediv__, __floordiv__, __mod__, __divmod__, __lshift__, __rshift__, __and__, __xor__, __or__, and __pow__

Numeric conversion methods: __complex__, __int__, __float__ and __index__

Descriptor methods: __get__, __set__ and __delete__

Pickling: __reduce__, __reduce_ex__, __getinitargs__, __getnewargs__, __getstate__ and __setstate__

File system path representation: __fspath__

Asynchronous iteration methods: __aiter__ and __anext__
```

- So, if you want to be on safer side, and don't want to implement them for every Mock object, directly use `MagicMock`.

!!! danger "**`MagicMock`** v/s **`Mock`**"
    - With `Mock` you can mock magic methods but you have to define them.
    - `MagicMock` has "default implementations of most of the magic methods.".
    - If you don't need to test any magic methods, `Mock` is adequate and doesn't bring a lot of extraneous things into your tests.
    - If you need to test a lot of magic methods `MagicMock` will **save you some time (and less bloated)**.

---

## `patch` decorators

- The patch decorators are used for patching objects only within the scope of the function they decorate.
- They automatically handle the unpatching for you, even if exceptions are raised.
- All of these functions can also be used in with statements or as class decorators.

---

### `@patch()`

- `patch` decorator can be used to modify some `target` temporarily.
- Pass in the path to `target`. `target` should be a string in the form `package.module.ClassName`.
- The `target` is imported and the specified object replaced with the new object, so the target must be importable from the environment you are calling patch() from. The target is imported when the decorated function is executed, not at decoration time.

- You can either specify a `patched value`, or by default it will be a `Mock object`.
- The function, if wants to access mock object, need to specify a parameter in **reverse** order of `@patch` chains.

```python
@patch('__main__.SomeClass2')
@patch('__main__.SomeClass1')
def function(normal_argument, mock_class1, mock_class2):
    print(mock_class1 is SomeClass1)
    print(mock_class2 is SomeClass2)

function(None)
```

- To patch with some value:

```python
@patch("litdata.streaming.downloader._GOOGLE_STORAGE_AVAILABLE", True)
def test_gcp_downloader(tmpdir, monkeypatch):
    ... # you code
```

---

### `@patch.object`

- Very similar, but for class methods.
- First parameter: target, second parameter: attribute.

```python
@patch.object(SomeClass, 'class_method')
def test(mock_method):
    SomeClass.class_method(3)
    mock_method.assert_called_with(3)

test()
```

---

### `@patch.dict`

- Patch a dictionary, or dictionary like object, and restore the dictionary to its original state after the test.

- If `clear is true`, then the `dictionary will be cleared` before the new values are set.

```python
foo = {}
@patch.dict(foo, {'newkey': 'newvalue'})
def test():
    assert foo == {'newkey': 'newvalue'}

test()
assert foo == {}
```

---

## Mocking a library, even if it's not available

- Create a `fixture` that create a **ModuleType** object, and monkeypatch to `sys.modules`.

```python
import pytest
import sys
from types import ModuleType


@pytest.fixture
def google_mock(monkeypatch):
    google = ModuleType("google")
    monkeypatch.setitem(sys.modules, "google", google)
    google_cloud = ModuleType("cloud")
    monkeypatch.setitem(sys.modules, "google.cloud", google_cloud)
    google_cloud_storage = ModuleType("storage")
    monkeypatch.setitem(sys.modules, "google.cloud.storage", google_cloud_storage)
    google.cloud = google_cloud
    google.cloud.storage = google_cloud_storage
    return google
```

- Use the fixture, and make module a `Mock` object

```python
@mock.patch("litdata.streaming.downloader._GOOGLE_STORAGE_AVAILABLE", True)
def test_gcp_downloader(tmpdir, monkeypatch, google_mock):
    # Create mock objects
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_blob.download_to_filename = MagicMock()

    # Patch the storage client to return the mock client
    google_mock.cloud.storage.Client = MagicMock(return_value=mock_client)

    # Configure the mock client to return the mock bucket and blob
    mock_client.bucket = MagicMock(return_value=mock_bucket)
    mock_bucket.blob = MagicMock(return_value=mock_blob)

    # Initialize the downloader
    storage_options = {"project": "DUMMY_PROJECT"}
    downloader = GCPDownloader("gs://random_bucket", tmpdir, [], storage_options)
    local_filepath = os.path.join(tmpdir, "a.txt")
    downloader.download_file("gs://random_bucket/a.txt", local_filepath)

    # Assert that the correct methods were called
    google_mock.cloud.storage.Client.assert_called_with(**storage_options)
    mock_client.bucket.assert_called_with("random_bucket")
    mock_bucket.blob.assert_called_with("a.txt")
    mock_blob.download_to_filename.assert_called_with(local_filepath)
```
