# OpenCV (cv2) - Computer Vision Library

## Installation

```bash
pip install opencv-python
```

---

## Load & display an image

```python
import cv2

# Load image (in BGR format by default)
img = cv2.imread('path/to/image.jpg')

# Display the image in a window
cv2.imshow('Image', img)
cv2.waitKey(0) # how many milliseconds to wait for a key press (0 = wait indefinitely)
cv2.destroyAllWindows()
```

---

## Convert BGR to RGB or Grayscale

```python
# Convert BGR to RGB (e.g., for plotting with matplotlib)
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Convert to grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

---

## Resize & reshape

```python
# Resize to 256x256
resized = cv2.resize(img, (256, 256))

# Reshape to 1D array (not usually needed unless flattening)
flattened = img.reshape(-1)
```

---

## Blur & smoothing

```python
# Gaussian blur
blurred = cv2.GaussianBlur(img, (5, 5), 0)

# Median blur
median = cv2.medianBlur(img, 5)

# Bilateral filter (preserves edges)
bilateral = cv2.bilateralFilter(img, 9, 75, 75)
```

---

## Basic transformations

```python
# Flip image (0 = vertical, 1 = horizontal, -1 = both)
flipped = cv2.flip(img, 1)

# Rotate image 90 degrees clockwise
rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# Crop (slicing)
cropped = img[50:200, 100:300]
```

---

## Save an image

```python
cv2.imwrite("output.jpg", img)
```
