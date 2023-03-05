# User Guide

## Installing `genid`

`genid` can be installed from [pypi](https://pypi.org/project/genid) using `pip`:

```bash
python -m pip install genid
```

## Introduction

Let's imagine that we have some code that rely on ID generation:

```python
class MyEntity:
    id: str


class MyUseCase:
    def create_entity() -> MyEntity:
        # How should ID be created ?
        # new_entity = MyEntity(id=???)
        # Can we write code agnostic to ID format ?
        raise NotImplementedError
```

`genid` can help in such situations by providing:

- A `IDGenerator` abstract class which can be used to annotate functions parameters
- Several implementations to use as generators

The example above could be written as follow:

```python
class MyUseCase:
    def __init__(id_generator: IDGenerator) -> None:
        # Use case must be created with an implementation of ID generator"""
        self._ids = id_generator

    def create_entity() -> MyEntity:
        # Create a new ID using `IDGenerator.new()` method
        new_id = self._ids.new()
        # Create an entity using the id
        return MyEntity(id=new_id)
```

In order to call the use case, an implementation of `IDGenerator` must now be provided:

```python
from genid import generator


# Create an ObjectID generator
generator = generator("objectid")
# Use the generator in order to initialize use case
use_case = MyUseCase(generator)
# Now it's possible to execute the use case
new_entity = use_case.create_entity()
# Entity ID is a valid ObjectID (example: "6404ec25f1421b11d772e6fb")
print(new_entity.id)
```

## ID Generators

The next section details the ID generators found in `genid` library.
