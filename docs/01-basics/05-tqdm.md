# TQDM

```bash
pip install tqdm
```

---

## Basic usage

```python
from tqdm import tqdm
for i in tqdm(range(10000)):
    ...
```

---

## Manually update `tqdm`

```python
import random
import time
from tqdm.auto import tqdm as _tqdm

total = 10

pbar = _tqdm(
    desc="Progress",
    total=total,
    smoothing=0,
    position=-1,
    mininterval=1,
    leave=True,
    dynamic_ncols=True,
    unit="step"
)

for _ in range(10):
    sleep_time = random.uniform(1, 1.5)  # Random sleep time between 0.5 and 1 second
    time.sleep(sleep_time)
    pbar.update(1)

pbar.close()
```
