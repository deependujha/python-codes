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
