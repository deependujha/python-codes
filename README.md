# Python helpful codes

1. Import library

```python
import sys
import os

# Get the current directory (where dummy.py is located)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the src directory
src_path = os.path.join(current_dir, '../litdata/src')

# Add the src directory to sys.path
sys.path.append(src_path)
import litdata
```
