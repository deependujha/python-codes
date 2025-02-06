# Pytest Installation & Configuration

## Install

```bash
pip install -U pytest

pytest --version
```

---

## Running pytest

```bash
# run testfile
pytest test_file_name.py

# run testfile in some nested dir
pytest test_dir1/test_dir2/test_file.py

# running a specific test
pytest test_dir1/test_file.py::my_test_name

# Specifying a specific test method
pytest tests/test_mod.py::TestClass::test_method

# Specifying a specific parametrization of a test
pytest tests/test_mod.py::test_func[x1,y2]

# marker expressions: run all tests decorated with `@pytest.mark.slow`
pytest -m slow

# marker expression: `@pytest.mark.slow(phase=1)`
pytest -m "slow(phase=1)"
```

!!! info "pytest options"  
    - `-q`: Run in quiet mode (minimal output).  
    - `-v`: Run in verbose mode (detailed output).  
    - `-s` (stdout): Disable output capturing (prints `print()` statements).  
    - `--tb=short`: Show a shortened traceback for test failures.  
    - `-k "expression" (keyword)`: Run tests matching the given substring or expression.

---

## Test discovery rule

!!! secondary "standard test discovery"
    - If no arguments are specified then collection starts from **`testpaths`** (if configured in `pyproject.toml` or `pytest.ini`), or the current directory.
    - Recurse into directories, unless they match **`norecursedirs`**.
    - In those directories, search for `test_*.py` or `*_test.py` files.
    - From those files, collect test items:
        - functions with `test` prefixed name. e.g., `test_is_valid`, etc.
        - Methods with `test` prefixed name inside Classes with name `Test{ClassName}` without `__init__` method.
        - Methods decorated with `@staticmethod` and `@classmethods` are also considered in classes with `Test` prefixed name and without `__init__`.

---

## Pytest Configuration

To get help on command line options and values in INI-style configurations files by using the general help option:

```bash
pytest -h   # prints options _and_ config file settings
```

> This will display command line and configuration file settings which were registered by installed plugins.

- We can specify pytest configurations in either `pytest.ini`, or `.pytest.ini` (hidden file), or `pyproject.toml` file.
- `pytest.ini` files take precedence over other files, even when empty.

- sample `pytest.ini` file

```ini
# pytest.ini or .pytest.ini
[pytest]
minversion = 6.0
addopts = -ra -q
testpaths =
    tests
    integration
```

- sample `pyproject.toml` pytest config

```toml
# pyproject.toml
[tool.pytest.ini_options]
minversion = "6.0"
testpaths = [
    "tests",
]
norecursedirs = [
    ".git",
    ".github",
    "dist",
    "build",
    "docs",
]
addopts = [
    "--strict-markers",
    "--doctest-modules",
    "--color=yes",
    "--disable-pytest-warnings",
    "--ignore=legacy/checkpoints",
]
markers = [
    "cloud: Run the cloud tests for example",
]
filterwarnings = [
    "error::FutureWarning",
]
xfail_strict = true
junit_duration_report = "call"
```

!!! success "Explanation of some pytest config options"
    - **`minversion = "6.0"`** → Requires pytest version 6.0 or higher.  
    - **`testpaths`** → Specifies directories or files where pytest should look for tests, improving test discovery performance.
    - **`norecursedirs`** → Prevents pytest from searching for tests in specified directories.  
    - **`addopts`** → Additional command-line options for pytest execution.  
        - `--strict-markers` → Enforces strict marker usage; unregistered markers cause errors.  
        - `--doctest-modules` → Runs doctests in all modules.  
        - `--color=yes` → Enables colored output in pytest results.  
        - `--disable-pytest-warnings` → Suppresses pytest-specific warnings.  
        - `--ignore=legacy/checkpoints` → Ignores the specified directory when discovering tests.  
    - **`markers`** → Defines custom markers like `cloud` for categorizing tests.  
    - **`filterwarnings`** → Converts `FutureWarning` to an error, ensuring deprecated features are addressed.  
    - **`xfail_strict = true`** → Treats all `xfail` tests as failures if they unexpectedly pass.  
    - **`junit_duration_report = "call"`** → Includes test call durations in JUnit XML reports.

---

## Recommended project structure

```txt
pyproject.toml
src/
    mypkg/
        __init__.py
        app.py
        view.py
tests/
    test_app.py
    test_view.py
    ...
```

To run tests:

- First install project in `editable mode.`

```bash
pip install -e .
```

- then, run tests

```bash
pytest # and provide options or use config file (pytest.ini or pyproject.toml)
```
