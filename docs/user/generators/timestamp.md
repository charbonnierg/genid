
# `TimestampGenerator`


A generator which produces **Unix timestamps**.

!!! tip
    Unix timestamps are number of seconds that have elapsed since 00:00:00 UTC on 1 January 1970.


## Examples

- Using the [`TimestampGenerator`](/reference/genid/#timestampgenerator){target=_blank} class:

```python
from genid import TimestampGenerator
import datetime


# Create a new generator
gen = TimestampGenerator()
# Generate new ID (timestamp as string)
new_id = gen.new()
# Check that new ID can be converted into a datetime
new_id_as_date = datetime.from_timestamp(int(new_id))
```

- Using the `generator` factory:

```python
from genid import generator, Kind

# Create a new generator
gen = generator(Kind.TIMESTAMP)
# A literal can also be used
gen = generator("timestamp")
# Generate new ID (timestamp as string)
new_id = gen.new()
# Check that new ID can be converted into a datetime
new_id_as_date = datetime.from_timestamp(int(new_id))
```
