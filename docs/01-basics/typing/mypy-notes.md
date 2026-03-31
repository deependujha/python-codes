# Pydantic + mypy (Practical Patterns)

## Why this combo is tricky

- Pydantic → runtime validation
- mypy → static analysis

👉 mismatch:
- Pydantic allows coercion
- mypy assumes strict types

---

## 1. Basic Compatibility

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int

u = User(id=1)

reveal_type(u.id)  # int ✅
````

Works fine because fields are properly typed.

---

## 2. The "Optional Hell"

```python
from typing import Optional

class Service:
    def __init__(self) -> None:
        self.user: Optional[User] = None

    def init(self) -> None:
        self.user = User(id=1)

    def run(self) -> int:
        return self.user.id  # ❌ mypy error
```

### ✅ Fix 1: Assert

```python
def run(self) -> int:
    assert self.user is not None
    return self.user.id
```

---

### ✅ Fix 2: Guard clause (cleaner)

```python
def run(self) -> int:
    if self.user is None:
        raise RuntimeError("Not initialized")
    return self.user.id
```

---

### ✅ Fix 3: Private + property (best pattern)

```python
class Service:
    def __init__(self) -> None:
        self._user: Optional[User] = None

    @property
    def user(self) -> User:
        if self._user is None:
            raise RuntimeError("Not initialized")
        return self._user
```

👉 Now:

* internal = Optional
* external = always safe

---

## 3. model_validate() vs constructor

```python
data: dict[str, object]

user = User(**data)              # ❌ mypy complains
user = User.model_validate(data) # ✅ preferred
```

👉 Why:

* constructor expects exact types
* `model_validate` is designed for unknown input

---

## 4. Typed dict → Pydantic

```python
from typing import TypedDict

class UserDict(TypedDict):
    id: int
    name: str

def create_user(data: UserDict) -> User:
    return User(**data)  # ✅ safe now
```

---

## 5. Avoid "Any leakage"

Bad:

```python
data = get_data()  # type: Any
user = User.model_validate(data)
```

Better:

```python
def get_data() -> dict[str, object]:
    ...
```

Best:

```python
def get_data() -> UserDict:
    ...
```

---

## 6. Validators + typing

```python
from pydantic import field_validator

class User(BaseModel):
    age: int

    @field_validator("age")
    def check_age(cls, v: int) -> int:
        return v
```

👉 Always type `v` and return type.

---

## 7. Computed fields are invisible to mypy

```python
class User(BaseModel):
    first: str
    last: str

    @property
    def full(self) -> str:
        return f"{self.first} {self.last}"
```

👉 mypy sees it fine only if it's a normal property
Avoid relying on `@computed_field` for typing logic.

---

## 8. Extra fields safety

```python
class User(BaseModel):
    model_config = {"extra": "forbid"}
```

👉 Helps catch bugs early (also aligns with mypy expectations)

---

## 9. Strict mode for sanity

```python
class User(BaseModel):
    model_config = {"strict": True}
    id: int
```

👉 Prevents silent coercion → matches mypy expectations

---

## 10. Lists & defaults

```python
from pydantic import Field

class Good(BaseModel):
    items: list[int] = Field(default_factory=list)
```

👉 mypy + runtime safe

---

## 11. Pattern: Boundary vs Core

```python
# boundary (Pydantic)
class UserModel(BaseModel):
    id: int
    name: str

# core (pure Python)
class User:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
```

Convert once:

```python
def to_domain(u: UserModel) -> User:
    return User(id=u.id, name=u.name)
```

👉 This avoids mixing runtime + static worlds

---

## 12. When mypy fights you

### ❌ Don’t do this:

```python
user = User.model_validate(data)
user.id + "abc"  # runtime fine? maybe, but mypy catches it
```

### ✅ Trust mypy more than Pydantic

👉 If they disagree → fix your types, not suppress errors

---

## 13. 🐢 mypy config (important)

- `pyproject.toml`

```toml
[tool.mypy]
files = [ "src" ]
exclude = [  ]
install_types = true
non_interactive = true
disallow_untyped_defs = true
ignore_missing_imports = true
show_error_codes = true
warn_redundant_casts = true
warn_unused_configs = true
warn_unused_ignores = true
allow_redefinition = true
disable_error_code = "attr-defined"
warn_no_return = false

[[tool.mypy.overrides]]
# generate with:
# mypy --no-error-summary 2>&1 | tr ':' ' ' | awk '{print $1}' | sort | uniq | sed 's/\.py//g; s|src/||g; s|\/|\.|g'
module = [  ]
ignore_errors = true
```

---

## 14. Useful trick: cast (last resort)

```python
from typing import cast

user = cast(User, something)
```

👉 Use only when you are 100% sure

---

## TL;DR

* Use Pydantic at boundaries (input/output)
* Keep core logic strictly typed
* Prefer `model_validate` over constructor for unknown data
* Kill `Optional` early (assert / guard / property)
* Avoid `Any` leaking

---

## Mental Model

Pydantic = runtime safety
mypy = compile-time safety

👉 You want BOTH, but clearly separated

```
