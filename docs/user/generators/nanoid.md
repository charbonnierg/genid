
# `NanoIDGenerator`


A generator producing **Nano ID** values. By default, Nano IDs are composed of 21 characters.

!!! tip
    [Learn more about Nano ID on Nano Collision ID Calculator application](https://zelark.github.io/nano-id-cc/){target=_blank}


## Examples

- Using the [`NanoIDGenerator`](/reference/genid/#nanoidgenerator){target=_blank} class:

```python
from genid import NanoIDGenerator

# Create a new generator
gen = NanoIDGenerator()
# Create a new nano id
nanoid = gen.new()
```

- Using the `generator` factory:

```python
from genid import generator, Kind

# Create a new generator
gen = generator(Kind.NANOID)
# A literal can also be used
gen = generator("nanoid")
# Create a new nano id
nanoid = gen.new()
```
