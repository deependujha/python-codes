# IO & BytesIO in Python

Python's built-in `io` module provides tools for handling **text** and **binary** streams efficiently.

## **Types of Streams**

1. **Text I/O (`TextIOBase`)** → Handles text files (`.txt`, `.csv`, etc.).
2. **Binary I/O (`BufferedIOBase`)** → Handles binary files (`.png`, `.mp4`, `.zip`, etc.).
3. **Raw I/O (`RawIOBase`)** → Low-level access to files & devices.
4. **In-Memory Streams (`BytesIO`, `StringIO`)** → Simulate file-like objects in RAM.

---

## `BytesIO`

`io.BytesIO` is a file-like object that operates in memory instead of disk.

- **Creating a `BytesIO` Object**

```python
import io

# Creating a BytesIO object with binary data
byte_stream = io.BytesIO(b"Hello, this is binary data!")

# Read the data
print(byte_stream.read())  # Output: b'Hello, this is binary data!'
```

- **Writing to `BytesIO`**

```python
byte_stream = io.BytesIO()
byte_stream.write(b"Python BytesIO Example")

# Reset cursor to the beginning before reading
byte_stream.seek(0)
print(byte_stream.read())  # Output: b'Python BytesIO Example'
```

- **Using `BytesIO` Like a File**

```python
with io.BytesIO() as byte_file:
    byte_file.write(b"Hello World!")
    byte_file.seek(0)  # Move back to start
    print(byte_file.read())  # Output: b'Hello World!'
```

### Writing `BytesIO` to a File

- **1️⃣ Using `.getvalue()`** (For small data)

```python
byte_stream = io.BytesIO(b"Binary Content")

with open("output.bin", "wb") as f:
    f.write(byte_stream.getvalue())  # Extract all bytes and write to file
```

- **2️⃣ Using `shutil.copyfileobj()`** (For large data)

```python
import shutil

byte_stream = io.BytesIO(b"Large binary content...")

with open("output_large.bin", "wb") as f:
    shutil.copyfileobj(byte_stream, f)  # Efficient copy without memory overhead
```

---

## Reading & Writing Binary Files with `open()`

```python
# Writing binary data to a file
with open("data.bin", "wb") as f:
    f.write(b"Some binary data")

# Reading binary data from a file
with open("data.bin", "rb") as f:
    content = f.read()
    print(content)  # Output: b'Some binary data'

# reading file in 1000 bytes chunks
with open("data.bin", "rb") as f:
    while chunk := f.read(1000):
        print(chunk)

# download from cloud and save in 1000 bytes chunks
with self.fs.open(_file["name"], "rb") as cloud_file, open(temp_path, "wb") as local_file:
    # b"" is the sentinel value, pause when you get empty bytes
    for chunk in iter(lambda: cloud_file.read(4096), b""):  # Read in 4KB chunks
        local_file.write(chunk)
```

---

## Seeking & Telling in Binary Streams

- **`seek(offset, whence)` → Move the file pointer**

- `whence=0` → Start from the beginning (default)
- `whence=1` → Move relative to current position
- `whence=2` → Move relative to the end

- **Example: Seeking & Reading in Chunks**

```python
with open("data.bin", "rb") as f:
    f.seek(5)  # Move to the 5th byte
    print(f.read(10))  # Read next 10 bytes
```

- **Get Current Position with `tell()`**

```python
with open("data.bin", "rb") as f:
    print(f.tell())  # Output: 0 (Start position)
    f.read(5)
    print(f.tell())  # Output: 5 (After reading 5 bytes)
```

- Using **truncate()** to modify the file size

io.truncate(size) is used to resize a file to a specific byte length. If size is smaller than the current file size, the file is truncated (cut off) at that point. If size is larger, the file is extended, and the new space is filled with null bytes (\x00). It is useful for clearing files or adjusting their length without rewriting them.

```python
with open("example.txt", "wb") as f:
    f.write(b"Hello, World!")
    f.truncate(5)  # File now contains only "Hello"
```

!!! warning "Downloading a very large file very fast 🚀"
    - To download a large file very fast, we can make a header request to get the file size bytes.
    - Create a file and preallocate the size.
    - Then start number of threads that will download their range in parallel.
    - After downloading, each thread will write their range to the file.

---

## Handling Large Files Efficiently

- **Using `seek()` & `read()` for Large Files**

```python
with open("large_file.bin", "rb") as f:
    chunk_size = 1024  # Read in 1KB chunks
    while chunk := f.read(chunk_size):
        process(chunk)  # Replace with your processing logic
```

---

## Using `mmap` for Efficient File Access

- **Memory-mapped File for Large Binary Data**

```python
import mmap

with open("large_file.bin", "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    print(mm[:100])  # Read first 100 bytes
    mm.close()
```

✅ **No RAM overhead even for 100GB+ files!**

---

## When to Use `BytesIO`?

!!! info ""
    - ✅ When you **don't want to use disk I/O** (temporary storage)
    - ✅ Handling **binary data manipulation in memory**
    - ✅ Simulating **file objects for APIs that expect file-like input**
