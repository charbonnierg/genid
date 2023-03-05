
# `ConstantIDGenerator`


A generator which always produce **the same ID value**.

!!! tip
    This generator is useful only during tests. It does not serve any other purpose than providing a predictable ID generator during tests.


## Examples

- Using the [`ConstantIDGenerator`](/reference/genid/#constantidgenerator){target=_blank} class:

```python
from genid import ConstantIDGenerator

# Create a new generator
gen = ConstantIDGenerator("test")
# Check that new ID is equal to value provided at init
assert gen.new() == "test"
```

- Using the `generator` factory:

```python
from genid import generator, Kind

# Create a new generator
gen = generator(Kind.CONSTANT, value="test")
# A literal can also be used
gen = generator("constant", value="test")
# Check that new ID is equal to value provided to factory
assert gen.new() == "test"
```
