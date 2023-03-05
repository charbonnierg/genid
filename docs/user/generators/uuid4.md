
# `UUID4Generator`


A generator producing **UUID4** values.

!!! tip
    [Learn more about UUIDs on the Python language documentation](https://docs.python.org/3/library/uuid.html#module-uuid){target=_blank}


## Examples

- Using the [`UUID4Generator`](/reference/genid/#uuid4generator){target=_blank} class:

```python
from genid import UUID4Generator

# Create a new generator
gen = UUID4Generator()
# Create a new object id
objectid = gen.new()
```

- Using the `generator` factory:

```python
from genid import generator, Kind

# Create a new generator
gen = generator(Kind.UUID4)
# A literal can also be used
gen = generator("uuid4")
# Create a new object id
objectid = gen.new()
```
