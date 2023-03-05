import typing as t

from genid.generators import IDGenerator


def test_counter(generator: IDGenerator[t.Any]) -> None:
    for i in range(10000):
        idx, _ = generator.new_at_index()
        assert i == idx
