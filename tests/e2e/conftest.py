import typing as t

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
        "ulid",
        "incremental",
        "secret",
        "timestamp",
        "nstimestamp",
    ]
)
def generator(request: SubRequest) -> IDGenerator[t.Any]:
    kind = request.param
    return _generator(kind)
