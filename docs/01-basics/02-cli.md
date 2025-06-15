# Command Line Interface (CLI)

- Assumes you already have a python project with `__init__.py` file and `pyproject.toml` or `setup.py` file.

```txt
src/
├── mylib/
│   ├── __init__.py
│   └── cli.py
└── pyproject.toml
└── setup.py
```

---

## Steps ⭐️

## Step 1: Create a CLI file

> Create a new file named `cli.py` in your library directory (e.g., `mylib/cli.py`). This file will contain the logic for your command line interface.

## Step 2: Implement the CLI logic

```python
# mylib/cli.py
import argparse
from mylib import main_logic  # your core logic

def main():
    parser = argparse.ArgumentParser(description="MyLib CLI")
    parser.add_argument("--input", type=str, required=True)
    args = parser.parse_args()
    
    result = main_logic(args.input)
    print(result)

if __name__ == "__main__":
    main()
```

## Step 3: Define a CLI Entry Point in `pyproject.toml` or `setup.py`

- We need to **`define which function should be called`** when the CLI command is executed. This is done by `specifying an entry point` in your `pyproject.toml` or `setup.py` file.

- For `pyproject.toml`:

```toml
[project.scripts]
mylib = "mylib.cli:main"
```

- For `setup.py`:

```python
entry_points={
    "console_scripts": [
        "mylib = mylib.cli:main"
    ],
}
```

## Step 4: Install your package

- Now if you install your package in editable mode using `pip install -e .` or use `pip install package_name`, you can run your CLI with the command:

```bash
mylib --input "your_input_value"
```

> This will execute the `entrypoint` that you defined in `pyproject.toml` or `setup.py`.

---

## Suggestions ✅

- **Use [argparse](https://docs.python.org/3/library/argparse.html)**: It is a powerful library for parsing command line arguments and options.
- **Use [click](https://click.palletsprojects.com/en/stable/)**: If you want a more advanced CLI, consider using the `click` library, which provides a more user-friendly interface for building command line applications.
- **Use [typer](https://typer.tiangolo.com/)**: If you prefer type hints and want to create a CLI with less boilerplate, consider using `typer`, which is built on top of `click` and provides a more Pythonic way to define command line interfaces.

---

## Testing CLI 🤓

- If you're using `typer`, you can test your CLI using the `CliRunner` from `typer.testing`.

[typer testing](https://typer.tiangolo.com/tutorial/testing/)

```python
from typer.testing import CliRunner

from litdata.cli import app

runner = CliRunner()


def test_litdata_help_command():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "LitData CLI" in result.output
    assert "cache" in result.output


def test_cache_path_command():
    result = runner.invoke(app, ["cache", "path"])
    assert result.exit_code == 0
    assert "Default cache directory" in result.output


def test_cache_clear_command(tmp_path, monkeypatch):
    result = runner.invoke(app, ["cache", "clear"])
    assert result.exit_code == 0
    assert "cleared" in result.output
```
