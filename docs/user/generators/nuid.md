
# `NUIDGenerator`


A generator producing **NUID** values.

!!! tip
    NUID is an implementation of the approach for fast generation of
    unique identifiers used for inboxes in NATS.
    [Learn more about NUID by looking at the original Go implemetation](https://github.com/nats-io/nuid){target=_blank}


## Examples

- Using the [`NUIDGenerator`](/reference/genid/#nuidgenerator){target=_blank} class:

```python
from genid import NUIDGenerator

# Create a new generator
gen = NUIDGenerator()
# Create a new nuid
nuid = gen.new()
```

- Using the `generator` factory:

```python
from genid import generator, Kind

# Create a new generator
gen = generator(Kind.NUID)
# A literal can also be used
gen = generator("nuid")
# Create a new nuid
nuid = gen.new()
```
