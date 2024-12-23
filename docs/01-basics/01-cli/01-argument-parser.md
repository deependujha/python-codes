# Argument Parser in Python

### **Python argparse - Concise Notes**

`argparse` is a Python library for parsing command-line arguments. It provides a simple interface to define, process, and handle arguments.

---

### **Basic Usage**

1. **Setup**
   ```python
   import argparse
   parser = argparse.ArgumentParser(description="A simple script")
   ```

2. **Adding Arguments**

   - **Positional Argument**: Required, order matters
     ```python
     parser.add_argument("filename", help="File to process")
     ```

   - **Optional Argument**: Starts with `--` or `-`, order doesn’t matter.
     ```python
     parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
     parser.add_argument("-n", "--number", type=int, default=1, help="Number of iterations")
     ```

3. **Parsing Arguments**

   ```python
   args = parser.parse_args()
   print(args.filename)      # Positional argument
   print(args.verbose)       # True/False (store_true)
   print(args.number)        # Integer value (default: 1)
   ```

---

### **Key Argument Settings**

1. **Positional Arguments**:
   - No special prefix.
   - Example: `python script.py input.txt`

2. **Optional Arguments**:
   - Use `-` or `--`.
   - Example: `python script.py --verbose`

3. **Argument Types**:
   - Specify with `type` (e.g., `int`, `float`, `str`).
   - Example:
     ```python

     parser.add_argument("--value", type=float, help="A float value")
     ```

4. **Default Values**:
   - Use `default`.
   - Example:
     ```python

     parser.add_argument("--name", default="User", help="Default name")
     ```

5. **Boolean Flags**:
   - Use `action="store_true"` or `action="store_false"`.
   - Example:

     ```python
     parser.add_argument("--debug", action="store_true", help="Enable debug mode")
     ```

---

### **Example Usage**

Script:

```python
import argparse

parser = argparse.ArgumentParser(description="Demo script")
parser.add_argument("filename", help="Input file name")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbosity")
parser.add_argument("-n", "--number", type=int, default=10, help="Number of items")
args = parser.parse_args()

print(f"Filename: {args.filename}")
print(f"Verbose: {args.verbose}")
print(f"Number: {args.number}")
```

Run:

```bash
python script.py file.txt --verbose -n 5
```

Output:

```
Filename: file.txt
Verbose: True
Number: 5
```

---

### **Common Methods**

1. `parser.add_argument()`: Define arguments.
2. `parser.parse_args()`: Parse command-line inputs.

---

### **Tips**

- Use `help` for clear CLI documentation.
- Default type is `str` if not specified.
- Boolean flags (`store_true`) are ideal for toggles.

For most cases, this basic usage suffices!
