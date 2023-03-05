
# `NanoSecondTimestampGenerator`


A generator which produces **Unix timestamps in nanoseconds**.

!!! tip
    Nanoseconds unit timestamps are number of nanoseconds that have elapsed since 00:00:00 UTC on 1 January 1970.


## Examples

- Using the [`NanoSecondTimestampGenerator`](/reference/genid/#nanosecondtimestampgenerator){target=_blank} class:

```python
from genid import NanoSecondTimestampGenerator
import datetime


# Create a new generator
gen = NanoSecondTimestampGenerator()
# Generate new ID (nanosecond timestamp as string)
new_id = gen.new()
# Check that new ID can be converted into a datetime
new_id_as_date = datetime.from_timestamp(int(new_id) / 1e9)
```

- Using the `generator` factory:

```python
from genid import generator, Kind

# Create a new generator
gen = generator(Kind.NSTIMESTAMP)
# A literal can also be used
gen = generator("nstimestamp")
# Generate new ID (nanosecond timestamp as string)
new_id = gen.new()
# Check that new ID can be converted into a datetime
new_id_as_date = datetime.from_timestamp(int(new_id) / 1e9)
```
