# Pillow (PIL fork) - Python Imaging Library

## Installation

```bash
pip install Pillow
```

---

## Loading & showing an Image

```python
from PIL import Image
# Load an image from a file
image = Image.open('path/to/image.jpg')
# Display the image
image.show()
```

---

## Get bytes of the image

```python
from PIL import Image
import io

# Load the image
img = Image.open("your_image.jpg")

# Save it into a bytes buffer
buffer = io.BytesIO()
img.save(buffer, format="JPEG")  # or "PNG", depending on your image

# Get the raw bytes
image_bytes = buffer.getvalue()

# Print the bytes (optional: limit how many you print)
print(image_bytes[:100])  # prints first 100 bytes for sanity
```

---

## Create a random dummy image

```python
from PIL import Image
import numpy as np

# Generate random RGB pixel data
random_pixels = np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)

# Convert to a PIL Image
img = Image.fromarray(random_pixels, 'RGB')

# Show the image (or save it if you want)
img.show()
# img.save("dummy_image.png")
```
