# Mark test functions with attributes

- By using the **`pytest.mark`** helper you can easily set metadata on your test functions.

---

## Some common markers

| **marker** | information |
| ---- | ---- |
| **usefixtures**  | use fixtures on a test function or class  |
| **filterwarnings**  | filter certain warnings of a test function  |
| **skip**  | always skip a test function  |
| **skipif**  | skip a test function if a certain condition is met  |
| **xfail**  | produce an “expected failure” outcome if a certain condition is met  |
| **parameterize**  | perform multiple calls to the same test function.  |

---

## `usefixtures`

- Sometimes test functions do not directly need access to a fixture object.
- So, rather than specifying in test function parameter, we simply mark it with `pytest.mark.usefixtures`.

```python
@pytest.mark.usefixtures("fixture_one", "another_fixture")
def test(): ...
```

---

## `filterwarnings`

- You can use the `@pytest.mark.filterwarnings` mark to add warning filters to specific test items, allowing you to have finer control of which warnings should be captured at test, class or even module level:

```python
import warnings


def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


@pytest.mark.filterwarnings("ignore:api v1")
def test_one():
    assert api_v1() == 1
```

- You can specify multiple filters with separate decorators:

```python
# Ignore "api v1" warnings, but fail on all other warnings
@pytest.mark.filterwarnings("ignore:api v1")
@pytest.mark.filterwarnings("error")
def test_one():
    assert api_v1() == 1
```

---

## `skip`

The simplest way to skip a test function is to mark it with the skip decorator which may be passed an optional reason:

```python
@pytest.mark.skip(reason="no way of currently testing this")
def test_the_unknown(): ...
```

- Alternatively, it is also possible to skip imperatively during test execution or setup by calling the pytest.skip(reason) function:

```python
def test_function():
    if not valid_config():
        pytest.skip("unsupported configuration")
```

---

## `skipif`

If you wish to skip something conditionally then you can use skipif instead.

```python
import sys

@pytest.mark.skipif(sys.platform == "win32", reason="windows isn't supported")
def test_dataset_for_text_tokens_with_large_num_chunks(tmpdir):
    import resource

    resource.setrlimit(resource.RLIMIT_NOFILE, (1024, 1024))

    block_size = 1024
    cache = Cache(input_dir=str(tmpdir), chunk_bytes="10KB", item_loader=TokensLoader(block_size))

    for i in range(10000):
        text_ids = torch.randint(0, 10001, (torch.randint(100, 1001, (1,)).item(),)).numpy()
        cache._add_item(i, text_ids)

    cache.done()
    cache.merge()

    dataset = StreamingDataset(input_dir=str(tmpdir), item_loader=TokensLoader(block_size), shuffle=True)

    for _ in dataset:
        pass
```

---

## `xfail`

- You can use the xfail marker to indicate that you expect a test to fail

```python
@pytest.mark.xfail
def test_function(): ...
```

- Alternatively, you can also mark a test as XFAIL from within the test or its setup function imperatively

```python
def test_function():
    if not valid_config():
        pytest.xfail("failing configuration (but should work)")

# ------

def test_function2():
    import slow_module

    if slow_module.slow_function():
        pytest.xfail("slow_module taking too long")
```

- `xfail` conditionally

```python
@pytest.mark.xfail(sys.platform == "win32", reason="bug in a 3rd party library")
def test_function(): ...
```

- `xfail` with a specific exception

```python
@pytest.mark.xfail(raises=RuntimeError)
def test_function(): ...
```

- If a test should be marked as xfail and reported as such but `should not be even executed`, use the **`run`** parameter as `False`:

```python
@pytest.mark.xfail(run=False)
def test_function(): ...
```

!!! `strict=True` in `xfail`
    - Both `XFAIL` and `XPASS` **don’t fail the test suite by default**.
    - With `strict=True`, **`XPASS (“unexpectedly passing”)`** results from this test to **fail the test suite**.

    ```python
    @pytest.mark.xfail(strict=True)
    def test_function(): ...
    ```

---

## **`Skip/xfail with parametrize`**

- It is possible to apply markers like skip and xfail to individual test instances when using parametrize:

```python
import sys

import pytest


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, 2),
        pytest.param(1, 0, marks=pytest.mark.xfail),
        pytest.param(1, 3, marks=pytest.mark.xfail(reason="some bug")),
        (2, 3),
        (3, 4),
        (4, 5),
        pytest.param(
            10, 11, marks=pytest.mark.skipif(sys.version_info >= (3, 0), reason="py2k")
        ),
    ],
)
def test_increment(n, expected):
    assert n + 1 == expected
```
