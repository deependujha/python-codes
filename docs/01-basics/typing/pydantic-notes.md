# Pydantic Notes (Quick + Practical)

## What is Pydantic?

- Data validation + parsing using Python type hints
- Core class: `BaseModel`
- Think: **typed schema + runtime validation**

### What is `BaseModel`?

- `BaseModel` is the core class in the Pydantic library used to define `data models`.
- By inheriting from BaseModel, you create classes that automatically perform `data parsing`, `validation`, and `serialization` based on Python type annotations.

---

## Installation

```bash
uv pip install pydantic
```

---

## Creating Model & Validation

```python
from uuid import uuid4
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated


class User(BaseModel):
    model_config = ConfigDict(strict=True)

    id: str = Field(default_factory=lambda: uuid4().hex)

    name: str = Field(..., max_length=15, frozen=True)
    email: EmailStr = Field(...)
    is_subscribed: Annotated[bool, Field(default=False, description="Indicates if subscribed to the newsletter")]
    age: Annotated[int, Field(gt=18, lt=70, description="The age of the user")]
    friends: Annotated[tuple[str, ...], Field(default_factory=tuple, description="List of friends' names", frozen=True)]
    contacts: Annotated[dict[str, str], Field(default_factory=dict, description="dict containing name to contact number")]


user = User(id=1, name="Alice", email="alicel@gmail.com", age=30, friends=("Dave",))
```

- To create a model, define a class that inherits from `BaseModel` and use type annotations for fields.
- Pydantic will automatically validate the input data based on the types and constraints defined in the model.
- To specify field constraints and metadata, you can use the `Field` function, and to specify model-level configuration, you can use the `ConfigDict` class, and must be assigned to the `model_config` attribute of the model class.

---

## More on fields & config

- Elipsis (`...`) is used to indicate that a field is required and must be provided when creating an instance of the model. If a required field is missing, Pydantic will raise a `ValidationError`. It is optional, and even if you don't use it, the field will still be required by default. However, using `...` can make it more explicit that the field is required. It is also discouraged in many projects, as it can be less readable and may not provide any additional benefits over simply omitting the default value.

- `gt` and `lt` are used for numeric fields to specify greater than and less than constraints, respectively.
- `max_length` is used to specify the maximum length of a string field.
- `default_factory` is used to provide a default value for mutable types like lists or tuples. `frozen=True` makes the field immutable after creation.
- `EmailStr` is a special type that validates email addresses. There're many similar built-in types for validation like: `AnyHttpUrl, AnyUrl, IPvAnyAddress, IPvAnyNetwork, IPvAnyInterface, FilePath, DirectoryPath, Json, SecretStr, SecretBytes`
- `strict=True` in `model_config` ensures that no type coercion happens, and the input must match the declared type exactly. `frozen=True` in `model_config` makes the entire model immutable after creation.

---

## Type Coercion vs Strict

```python
User(id="123", name="test")  # OK (coerced)
User(id="abc", name="test")  # ❌ ValidationError
```

**Strict mode**:

- in strict mode, no coercion happens. The input must match the declared type exactly.

- We can either make a single field strict using `strict=True` in the field definition,

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., strict=True)

User(id="123", name="test")  # ❌ ValidationError
```

- or make the entire model strict using `model_config`.

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(strict=True)
    id: int

User(id="123", name="test")  # ❌ ValidationError
```

---

## Frozen fields & models

- A frozen field is defined with `frozen=True` in the `Field` definition, making that specific field immutable after the model instance is created.
- To make the entire model immutable, you can set `frozen=True` in the `model_config`. This means that all fields in the model will be immutable after creation.

> Remember: frozen fields and models block attribute assignment after creation, but they do not prevent mutation of inner objects-> mutable types (like `lists` or `dicts`) if they are not frozen themselves. To make a field truly immutable, you should use an immutable type (like `tuple` instead of `list`) for that specific field. 

```python
from pydantic import BaseModel, ConfigDict, Field

class User1(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: int
    name: str

class User2(BaseModel):
    id: int
    name: str = Field(..., frozen=True)

user = User1(id=123, name="test") 
user.name = "new_name"  # ❌ ValidationError (instance is frozen)

user = User2(id=123, name="test") 
user.name = "new_name"  # ❌ ValidationError (field is frozen)
```

---

## Annotated Fields

- For some type checkers, this syntax `some_name: type = Field(...)` may seem like an assignment, which can cause issues.
- to avoid this, we can use `Annotated` from the `typing` module to separate the type annotation from the field definition.

```python
from pydantic import BaseModel, Field
from typing import Annotated

class User(BaseModel):
    id: Annotated[int, Field(..., description="unique identifier")]
    name: Annotated[str, Field(..., max_length=15, frozen=True)]
    email: EmailStr
    is_subscribed: Annotated[bool, Field(default=False, description="Indicates if subscribed to the newsletter")]

user = User(id=1, name="Alice", email="alice@gmail.com", is_subscribed=True)
```

- **Use Annotated in Pydantic to bind validation, metadata, or serialization logic directly to a type**

```python
from typing import Annotated
from pydantic import BaseModel, Field, AfterValidator

# Create a reusable constrained type
PositiveInt = Annotated[int, Field(gt=0)]

# Use in a model
class Product(BaseModel):
    # Apply validation directly to the field
    id: PositiveInt
    # directly bind a transformation to the field, without needing a separate field_validator method
    price: Annotated[float, AfterValidator(lambda x: round(x, 2))]
```

---

## Field Validator

- a `field_validator` is a callable taking the value to be vaildated as an argument returning the validated value or raising a `ValueError` if validation fails. It is used to perform custom validation logic on individual fields.

- It has 4 different modes: `before`, `after`, `wrap`, and `plain`.
    - The default is `after`, which means the validator will be called after the standard validation and parsing logic has been applied to the field. In this mode, the validator receives the already validated value, allowing you to perform additional checks or transformations on it.

=== "Annotated pattern"

    ```python
    from typing import Annotated

    from pydantic import AfterValidator, BaseModel, ValidationError


    def is_even(value: int) -> int:
        if value % 2 == 1:
            raise ValueError(f'{value} is not an even number')
        return value  


    class Model(BaseModel):
        number: Annotated[int, AfterValidator(is_even)]


    try:
        Model(number=1)
    except ValidationError as err:
        print(err)
        """
        1 validation error for Model
        number
        Value error, 1 is not an even number [type=value_error, input_value=1, input_type=int]
        """
    ```

=== "Decorator"

    ```python
    from pydantic import BaseModel, ValidationError, field_validator


    class Model(BaseModel):
        number: int

        @field_validator('number', mode='after')  
        @classmethod
        def is_even(cls, value: int) -> int:
            if value % 2 == 1:
                raise ValueError(f'{value} is not an even number')
            return value  


    try:
        Model(number=1)
    except ValidationError as err:
        print(err)
        """
        1 validation error for Model
        number
        Value error, 1 is not an even number [type=value_error, input_value=1, input_type=int]
        """
    ```

- `before` run before Pydantic's internal parsing and validation (e.g. coercion of a str to an int). These are more flexible than after validators, but they also have to deal with the raw input, which in theory could be any arbitrary object. You should also avoid mutating the value directly if you are raising a validation error later in your validator function, as the mutated value may be passed to other validators if using unions. The value returned from this callable is then validated against the provided type annotation by Pydantic.

=== "Annotated pattern"
    ```python
    from typing import Annotated, Any

    from pydantic import BaseModel, BeforeValidator, ValidationError


    def ensure_list(value: Any) -> Any:  
        if not isinstance(value, list):  
            return [value]
        else:
            return value


    class Model(BaseModel):
        numbers: Annotated[list[int], BeforeValidator(ensure_list)]


    print(Model(numbers=2))
    #> numbers=[2]
    try:
        Model(numbers='str')
    except ValidationError as err:
        print(err)  
        """
        1 validation error for Model
        numbers.0
        Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='str', input_type=str]
        """
    ```
=== "Decorator"

    ```python
    from typing import Any

    from pydantic import BaseModel, ValidationError, field_validator


    class Model(BaseModel):
        numbers: list[int]

        @field_validator('numbers', mode='before')
        @classmethod
        def ensure_list(cls, value: Any) -> Any:  
            if not isinstance(value, list):  
                return [value]
            else:
                return value


    print(Model(numbers=2))
    #> numbers=[2]
    try:
        Model(numbers='str')
    except ValidationError as err:
        print(err)  
        """
        1 validation error for Model
        numbers.0
        Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='str', input_type=str]
        """
    ```

- `plain` validators: act similarly to before validators but they terminate validation immediately after returning, so no further validators are called and Pydantic does not do any of its internal validation against the field type.

=== "Annotated pattern"
    ```python
    from typing import Annotated, Any

    from pydantic import BaseModel, PlainValidator


    def val_number(value: Any) -> Any:
        if isinstance(value, int):
            return value * 2
        else:
            return value


    class Model(BaseModel):
        number: Annotated[int, PlainValidator(val_number)]


    print(Model(number=4))
    #> number=8
    print(Model(number='invalid'))  
    #> number='invalid'
    ```

=== "Decorator"
    ```python
    from typing import Any

    from pydantic import BaseModel, field_validator


    class Model(BaseModel):
        number: int

        @field_validator('number', mode='plain')
        @classmethod
        def val_number(cls, value: Any) -> Any:
            if isinstance(value, int):
                return value * 2
            else:
                return value


    print(Model(number=4))
    #> number=8
    print(Model(number='invalid'))
    #> number='invalid'
    ```

- `wrap` validators: the most flexible of all. You can run code before or after Pydantic and other validators process the input, or you can terminate validation immediately, either by returning the value early or by raising an error. Such validators must be defined with a mandatory extra handler parameter: a callable taking the value to be validated as an argument. Internally, this handler will delegate validation of the value to Pydantic. You are free to wrap the call to the handler in a try..except block, or not call it at all.

=== "Annotated pattern"
    ```python
    from typing import Any

    from typing import Annotated

    from pydantic import BaseModel, Field, ValidationError, ValidatorFunctionWrapHandler, WrapValidator


    def truncate(value: Any, handler: ValidatorFunctionWrapHandler) -> str:
        try:
            return handler(value)
        except ValidationError as err:
            if err.errors()[0]['type'] == 'string_too_long':
                return handler(value[:5])
            else:
                raise


    class Model(BaseModel):
        my_string: Annotated[str, Field(max_length=5), WrapValidator(truncate)]


    print(Model(my_string='abcde'))
    #> my_string='abcde'
    print(Model(my_string='abcdef'))
    #> my_string='abcde'
    ```

=== "Decorator"
    ```python
    from typing import Any

    from typing import Annotated

    from pydantic import BaseModel, Field, ValidationError, ValidatorFunctionWrapHandler, field_validator


    class Model(BaseModel):
        my_string: Annotated[str, Field(max_length=5)]

        @field_validator('my_string', mode='wrap')
        @classmethod
        def truncate(cls, value: Any, handler: ValidatorFunctionWrapHandler) -> str:
            try:
                return handler(value)
            except ValidationError as err:
                if err.errors()[0]['type'] == 'string_too_long':
                    return handler(value[:5])
                else:
                    raise


    print(Model(my_string='abcde'))
    #> my_string='abcde'
    print(Model(my_string='abcdef'))
    #> my_string='abcde'
    ```

---

## Which validator pattern to use: `Annotated` vs `Decorator`

While both approaches can achieve the same thing, each pattern provides different benefits.

### Using the annotated pattern¶

- One of the key benefits of using the annotated pattern is to make validators reusable:

```python
from typing import Annotated

from pydantic import AfterValidator, BaseModel


def is_even(value: int) -> int:
    if value % 2 == 1:
        raise ValueError(f'{value} is not an even number')
    return value


EvenNumber = Annotated[int, AfterValidator(is_even)]


class Model1(BaseModel):
    my_number: EvenNumber


class Model2(BaseModel):
    other_number: Annotated[EvenNumber, AfterValidator(lambda v: v + 2)]


class Model3(BaseModel):
    list_of_even_numbers: list[EvenNumber]
```

---

### Using the decorator pattern

- One of the key benefits of using the field_validator() decorator is to apply the function to `multiple fields`.

```python
from pydantic import BaseModel, field_validator


class Model(BaseModel):
    f1: str
    f2: str

    @field_validator('f1', 'f2', mode='before')
    @classmethod
    def capitalize(cls, value: str) -> str:
        return value.capitalize()
```

- If you want the validator to apply to all fields (including the ones defined in subclasses), you can pass `*` as the field name argument.
- By default, the decorator will ensure the provided field name(s) are defined on the model. If you want to disable this check during class creation, you can do so by passing `False` to the `check_fields` argument. This is useful when the field validator is defined on a base class, and the field is expected to exist on subclasses.

---

## Model Validators (validating across multiple fields)

- Has 3 different modes: `before`, `after`, and `wrap`. The default is `after`, which means the validator will be called after all field validators and Pydantic's internal validation logic has been applied to the model.

```python
from pydantic import BaseModel, model_validator

class User(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self
```

- `before` & `wrap` modes work similarly to field validators, but they receive the entire input data as a dictionary instead of individual field values.

---

## Nested Models

```python
class User(BaseModel):
    id: int
    name: str

class Post(BaseModel):
    title: str
    author: User
```

---

## Parsing

```python
data = {"id": 1, "name": "Deependu"}

user = User(**data)
user = User.model_validate(data)
user.model_validate_json('{"id": 1, "name": "Deependu"}')
```

---

## Serialization

```python
user.model_dump() # returns dict of field values
user.model_dump_json() # returns JSON string of field values, you can write this string to a json file or send it over the network
```

---

## Aliases

```python
from pydantic import Field

class User(BaseModel):
    user_id: int = Field(alias="id")

User.model_validate({"id": 1})
```

---

## Computed Fields

```python
from pydantic import computed_field

class User(BaseModel):
    first: str
    last: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first} {self.last}"
```

---

## Config

```python
class User(BaseModel):
    model_config = {
        "extra": "forbid",   # forbid unknown fields
        "str_strip_whitespace": True
    }
```

---

## Extra Fields Handling

```python
class User(BaseModel):
    model_config = {"extra": "ignore"}  # or "allow", "forbid"
```

---

## Enums

```python
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    role: Role
```

---

## Common Use Cases

### 1. API Schemas (FastAPI)

```python
class Request(BaseModel):
    query: str
```

---

### 2. Config Management

```python
class Settings(BaseModel):
    debug: bool = False
    db_url: str
```

---

### 3. CLI Input Validation

```python
config = Settings(**vars(args))
```

---

### 4. Data Pipelines

```python
class Record(BaseModel):
    id: int
    value: float
```

---

## Performance Tip

* Avoid in tight loops
* Use for boundaries (I/O, API, configs)

---

## Gotchas

### 1. Silent coercion

```python
User(id="123")  # becomes int
```

→ Use strict mode if needed

---

### 2. Mutable defaults

```python
from typing import List

class Bad(BaseModel):
    items: List[int] = []  # ❌

class Good(BaseModel):
    items: List[int] = Field(default_factory=list)
```

---

### 3. Optional ≠ default None

```python
age: Optional[int]        # required
age: Optional[int] = None # optional
```

---

## When NOT to Use

* Hot paths / performance critical code
* Internal pure logic models

---

## Mental Model

* Boundary layer → ✅ use Pydantic
* Core logic → ❌ avoid

---

Good place to end — this is where you get **real control over behavior**.

Here are the **model_config options you’ll actually use in practice**, not the obscure ones.

---

# 🔥 Most Useful `model_config` Options

## 1. `strict=True` (highly recommended)

```python
model_config = ConfigDict(strict=True)
```

👉 disables coercion

```python
User(id="1")  # ❌ instead of silently becoming int
```

💡 Use this in almost all serious projects

---

## 2. `extra`

```python
model_config = ConfigDict(extra="forbid")
```

Options:

* `"ignore"` → drop unknown fields
* `"allow"` → keep them
* `"forbid"` → ❌ raise error

👉 Example:

```python
User(id=1, unknown="x")  # ❌ if forbid
```

💡 `"forbid"` is the cleanest default

---

## 3. `frozen=True`

```python
model_config = ConfigDict(frozen=True)
```

👉 makes model immutable (assignment blocked)

⚠️ does NOT prevent inner mutation

---

## 4. `str_strip_whitespace=True`

```python
model_config = ConfigDict(str_strip_whitespace=True)
```

👉 auto cleans input:

```python
User(name="  alice  ")  # → "alice"
```

---

## 5. `validate_assignment=True`

```python
model_config = ConfigDict(validate_assignment=True)
```

👉 re-validates on mutation

```python
user.age = "abc"  # ❌ ValidationError
```

💡 Useful if model is mutable

---

## 6. `populate_by_name=True`

```python
model_config = ConfigDict(populate_by_name=True)
```

Used with aliases:

```python
from pydantic import Field

class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(alias="id")

User(user_id=1)
User(id=1)
```

👉 both work

---

## 7. `use_enum_values=True`

```python
model_config = ConfigDict(use_enum_values=True)
```

👉 stores enum as raw value

```python
role = Role.admin  # → "admin"
```

---

## 8. `from_attributes=True`

```python
model_config = ConfigDict(from_attributes=True)
```

👉 allows parsing from objects (not just dicts)

```python
class Obj:
    id = 1

User.model_validate(Obj())
```

💡 very useful for ORM / scraping

---

## 9. `arbitrary_types_allowed=True`

```python
model_config = ConfigDict(arbitrary_types_allowed=True)
```

👉 lets you use custom classes

```python
class MyClass: ...

class Model(BaseModel):
    obj: MyClass
```

---

## 🧠 My “default stack” (practical)

If I were setting a base model:

```python
from pydantic import BaseModel, ConfigDict

class Base(BaseModel):
    model_config = ConfigDict(
        strict=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
```

👉 This alone removes a LOT of bugs

---

## ⚠️ Common mistakes

### ❌ forgetting `extra="forbid"`

→ silent bugs from unexpected fields

---

### ❌ using `strict=False` (default) blindly

→ weird coercions sneak in

---

### ❌ mixing frozen + mutation expectations

→ leads to confusing behavior

---

## 🧩 Mental model

`model_config` controls:

* **input behavior** → strict, extra
* **mutation behavior** → frozen, validate_assignment
* **parsing behavior** → from_attributes
* **data normalization** → strip whitespace

---

## 🚀 TL;DR

If you only remember 5:

* `strict=True`
* `extra="forbid"`
* `frozen=True` (optional)
* `validate_assignment=True` (if mutable)
* `str_strip_whitespace=True`
