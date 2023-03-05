
# `SecretIDGenerator`


A generator which produces **random hex strings**. By default, generated IDs are composed of 16 characters.

!!! tip
    This generator relies on the [`secrets.token_hex` function from the python standard library](https://docs.python.org/3/library/secrets.html#secrets.token_hex){target=_blank}. It can be used to generate random secret identifiers within applications.


## Examples

- Using the [`SecretIDGenerator`](/reference/genid/#secretidgenerator){target=_blank} class:

```python
from genid import SecretIDGenerator

# Create a new generator with default length (16)
gen = SecretIDGenerator()
# Create a new generator with custom length
gen = SecretIDGenerator(21)
# Generate and check that new ID length is 21 as expected
new_id = gen.new()
assert len() == 21
```

- Using the `generator` factory:

```python
from genid import generator, Kind

# Create a new generator
gen = generator(Kind.SECRET, length=21)
# A literal can also be used
gen = generator("secret", length=21)
# Generate and check that new ID length is 21 as expected
new_id = gen.new()
assert len() == 21
```
