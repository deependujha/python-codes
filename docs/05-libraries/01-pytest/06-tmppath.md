# `tmppath` fixture

- You can use the `tmp_path` fixture which will provide **`a temporary directory unique to each test function`**.
- `tmp_path` is a `pathlib.Path` object

```python
# content of test_tmp_path.py
CONTENT = "content"


def test_create_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(CONTENT, encoding="utf-8")
    assert p.read_text(encoding="utf-8") == CONTENT
    assert len(list(tmp_path.iterdir())) == 1
    assert 0
```
