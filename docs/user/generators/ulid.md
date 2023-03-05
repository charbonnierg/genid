
# `ULIDGenerator`


A generator producing **ULID** values.

!!! tip
    A ULID is a universally unique lexicographically sortable identifier. It is

    - 128-bit compatible with UUID

    - Lexicographically sortable!

    - Canonically encoded as a 26 character string, as opposed to the 36 character UUID

    - Uses Crockford’s base32 for better efficiency and readability (5 bits per character)

    - Case insensitive

    - No special characters (URL safe)

    In general the structure of a ULID is as follows:

    ```text
    01AN4Z07BY      79KA1307SR9X4MV3
    |----------|    |----------------|
    Timestamp          Randomness
    48bits             80bits
    ```

    For more information have a look at [the original specification](https://github.com/alizain/ulid#specification){target=_blank}.


## Examples

- Using the [`ULIDGenerator`](/reference/genid/#ulidgenerator){target=_blank} class:

```python
from genid import ULIDGenerator

# Create a new generator
gen = ULIDGenerator()
# Create a new ulid
ulid = gen.new()
```

- Using the `generator` factory:

```python
from genid import generator, Kind

# Create a new generator
gen = generator(Kind.ULID)
# A literal can also be used
gen = generator("ulid")
# Create a new ulid
ulid = gen.new()
```
