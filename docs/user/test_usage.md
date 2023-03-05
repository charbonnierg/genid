# Usage in tests

It's possible to write `pytest` fixtures in order to run a single tets case with several ID generators.

## Pytest fixture example

- Define a fixture which will provide several ID generators:

```python
import pytest
from _pytest.fixtures import SubRequest

from genid.generators import IDGenerator
from genid.generators import generator as _generator


@pytest.fixture(
    params=[
        "nanoid",
        "nuid",
        "objectid",
        "uuid1",
        "uuid4",
        "incremental",
        "secret",
        "timestamp",
        "nstimestamp",
    ]
)
def generator(request: SubRequest) -> IDGenerator:
    kind: str = request.param
    return _generator(kind)
```

- Write a test depending on the `generator` fixture:

```python
from genid.generators import IDGenerator


def test_something(generator: IDGenerator) -> None:
    """Test something which requires an ID."""
    new_id = generator.new()
    # Do something with new id...
```

- Execute the test using `pytest -vvv`, you should see several test cases being executed:

```console
collected 9 items

tests/examples/test_counter.py::test_counter[nanoid] PASSED                [ 11%]
tests/examples/test_counter.py::test_counter[nuid] PASSED                  [ 22%]
tests/examples/test_counter.py::test_counter[objectid] PASSED              [ 33%]
tests/examples/test_counter.py::test_counter[uuid1] PASSED                 [ 44%]
tests/examples/test_counter.py::test_counter[uuid4] PASSED                 [ 55%]
tests/examples/test_counter.py::test_counter[incremental] PASSED           [ 66%]
tests/examples/test_counter.py::test_counter[secret] PASSED                [ 77%]
tests/examples/test_counter.py::test_counter[timestamp] PASSED             [ 88%]
tests/examples/test_counter.py::test_counter[nstimestamp] PASSED           [ 100%]
```
