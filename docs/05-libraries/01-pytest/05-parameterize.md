# Parameterize tests

## Simple Usage

- pytest allows to easily parametrize test functions using `@pytest.mark.parametrize`.
- We can also set marks for individual parameterize test.

```python
# content of test_pytest_param_example.py
import pytest


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("3+5", 8),
        pytest.param("1+7", 8, marks=pytest.mark.basic),
        pytest.param("2+4", 6, marks=pytest.mark.basic, id="basic_2+4"),
        pytest.param(
            "6*9", 42, marks=[pytest.mark.basic, pytest.mark.xfail], id="basic_6*9"
        ),
    ],
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

---

## Chaining multiple `@pytest.mark.parametrize`

```python
# taken from litdata tests

@pytest.mark.parametrize("drop_last", [False, True])
@pytest.mark.parametrize(
    "compression",
    [
        pytest.param(None),
        pytest.param("zstd", marks=pytest.mark.skipif(condition=not _ZSTD_AVAILABLE, reason="Requires: ['zstd']")),
    ],
)
@pytest.mark.timeout(60)
def test_streaming_dataset_distributed_full_shuffle_odd(drop_last, tmpdir, compression):
    ... # test body
```

---

## Parametrizing conditional raising

```python
from contextlib import nullcontext

import pytest


@pytest.mark.parametrize(
    "example_input,expectation",
    [
        (3, nullcontext(2)),
        (2, nullcontext(3)),
        (1, nullcontext(6)),
        (0, pytest.raises(ZeroDivisionError)),
    ],
)
def test_division(example_input, expectation):
    """Test how much I know division."""
    with expectation as e:
        assert (6 / example_input) == e
```

---

## test `IDs` in parameterize

- pytest will build a string that is the test ID for each set of values in a parametrized test.

```python
# content of test_time.py

from datetime import datetime, timedelta

import pytest

testdata = [
    (datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1)),
    (datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1)),
]


@pytest.mark.parametrize("a,b,expected", testdata)
def test_timedistance_v0(a, b, expected):
    diff = a - b
    assert diff == expected


@pytest.mark.parametrize("a,b,expected", testdata, ids=["forward", "backward"])
def test_timedistance_v1(a, b, expected):
    diff = a - b
    assert diff == expected


def idfn(val):
    if isinstance(val, (datetime,)):
        # note this wouldn't show any hours/minutes/seconds
        return val.strftime("%Y%m%d")


@pytest.mark.parametrize("a,b,expected", testdata, ids=idfn)
def test_timedistance_v2(a, b, expected):
    diff = a - b
    assert diff == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        pytest.param(
            datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1), id="forward"
        ),
        pytest.param(
            datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1), id="backward"
        ),
    ],
)
def test_timedistance_v3(a, b, expected):
    diff = a - b
    assert diff == expected
```

!!! quote ""
    - In `test_timedistance_v0`, we let pytest generate the test IDs.
    - In `test_timedistance_v1`, we specified ids as a list of strings which were used as the test IDs. These are succinct, but can be a pain to maintain.
    - In `test_timedistance_v2`, we specified ids as a function that can generate a string representation to make part of the test ID.

- generated IDs for above parameterized tests:

```txt
$ pytest test_time.py --collect-only
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 8 items

<Dir parametrize.rst-205>
  <Module test_time.py>
    <Function test_timedistance_v0[a0-b0-expected0]>
    <Function test_timedistance_v0[a1-b1-expected1]>
    <Function test_timedistance_v1[forward]>
    <Function test_timedistance_v1[backward]>
    <Function test_timedistance_v2[20011212-20011211-expected0]>
    <Function test_timedistance_v2[20011211-20011212-expected1]>
    <Function test_timedistance_v3[forward]>
    <Function test_timedistance_v3[backward]>

======================== 8 tests collected in 0.12s ========================
```

- To run specific parameterized test with its `ID`:

```bash
pytest -k "forward"
```
