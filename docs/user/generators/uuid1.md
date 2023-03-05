
# `UUID1Generator`


A generator producing **UUID1** values.

!!! tip
    [Learn more about UUIDs on the Python language documentation](https://docs.python.org/3/library/uuid.html#module-uuid){target=_blank}


## Examples

- Using the [`UUID1Generator`](/reference/genid/#uuid1generator){target=_blank} class:

```python
from genid import UUID1Generator

# Create a new generator
gen = UUID1Generator()
# Create a new object id
objectid = gen.new()
```

- Using the `generator` factory:

```python
from genid import generator, Kind

# Create a new generator
gen = generator(Kind.UUID1)
# A literal can also be used
gen = generator("uuid1")
# Create a new object id
objectid = gen.new()
```
