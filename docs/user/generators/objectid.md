
# `ObjectIDGenerator`


A generator producing **BSON Object Id** values.

!!! tip
    [Learn more about Object ID in MongoDB documentation](https://www.mongodb.com/docs/manual/reference/method/ObjectId/){target=_blank}


## Examples

- Using the [`ObjectIDGenerator`](/reference/genid/#objectidgenerator){target=_blank} class:

```python
from genid import ObjectIDGenerator

# Create a new generator
gen = ObjectIDGenerator()
# Create a new object id
objectid = gen.new()
```

- Using the `generator` factory:

```python
from genid import generator, Kind

# Create a new generator
gen = generator(Kind.OBJECTID)
# A literal can also be used
gen = generator("objectid")
# Create a new object id
objectid = gen.new()
```
