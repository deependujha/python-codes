# Walrus Operator

The walrus operator `:=` is a new operator in Python 3.8 that **`assigns values to variables as part of an expression`**.

```python
numbers = [1, 2, 3, 4, 5]

while (n := len(numbers)) > 0:
    print(numbers.pop())

```

---

## Example 1

```python
sample_data = [
    {"userId": 1, "name": "rahul", "completed": False},
    {"userId": 1, "name": "rohit", "completed": False},
    {"userId": 1, "name": "ram", "completed": False},
    {"userId": 1, "name": "ravan", "completed": True}
]

print("With Python 3.8 Walrus Operator:")
for entry in sample_data:
    if name := entry.get("name"):
        print(f'Found name: "{name}"')

print("Without Walrus operator:")
for entry in sample_data:
    name = entry.get("name")
    if name:
        print(f'Found name: "{name}"')
```

---

## Example 2

```python
## The below example is without Walrus Operator
foods = list()
while True:
  food = input("What food do you like?: ")
  if food == "quit":
    break
    foods.append(food)

# Below Approach uses Walrus Operator
foods1 = list()
while (food := input("What food do you like:=  ")) != "quit":
    foods.append(food)

```
