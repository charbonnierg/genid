import abc
import enum
import threading
import typing as t
from secrets import token_hex
from time import time, time_ns
from uuid import UUID, uuid1, uuid4

from .nanoid import DEFAULT_ALPHABET, DEFAULT_SIZE, nanoid
from .nuid import NUID
from .objectid import ObjectID
from .ulid import ULID

T = t.TypeVar("T")
GeneratorT = t.TypeVar("GeneratorT", bound="IDGenerator[t.Any]")


class IDGenerator(t.Generic[T], metaclass=abc.ABCMeta):
    """Abstract base class for ID generators.

    Implementations must provide the `new_id()` method.
    Optionally, implementations can override the `new()` method in order
    to return a string based on generated id.
    """

    def __init__(self) -> None:
        self._count = 0
        self._counter_lock = threading.Lock()

    @abc.abstractmethod
    def unsafe_create_id(self) -> T:
        """Get a new ID. Object type can depend on implementation."""
        raise NotImplementedError

    @staticmethod
    def id_to_string(value: t.Any) -> str:
        """Transform ID into string."""
        return str(value)

    def unsafe_revert(self) -> None:
        """Revert side effect of last ID generation. Does nothing by default."""
        pass

    def new_id_at_index(self, idx: t.Optional[int] = None) -> t.Tuple[int, T]:
        """Get a tuple holding new ID index and new ID as an object.
        Object type can depend on implementation.
        """
        with self._counter_lock:
            _id = self.unsafe_create_id()
            _index = self._count
            if idx is not None and _index != idx:
                self.unsafe_revert()
                raise IndexError(
                    f"Cannot create ID with wrong index. Expected: {idx}. Got: {_index}"
                )
            self._count += 1
        return _index, _id

    def new(self) -> str:
        """Get a new ID as a string."""
        _, _id = self.new_id_at_index()
        return str(_id)

    def new_at_index(self, index: t.Optional[int] = None) -> t.Tuple[int, str]:
        """Get a tuple holding new ID index and new ID as string."""
        idx, _id = self.new_id_at_index(index)
        return idx, self.id_to_string(_id)

    def count(self) -> int:
        """Return total number of ID produced since generator was created."""
        return self._count

    def __iter__(self: GeneratorT) -> GeneratorT:
        return self

    def __next__(self) -> t.Tuple[int, str]:
        return self.new_at_index()


class ConstantIDGenerator(IDGenerator[str]):
    """An ID Generator which always return the same value.
    Can be useful within unit tests.
    """

    def __init__(self, value: str) -> None:
        super().__init__()
        self._value = value

    def unsafe_create_id(self) -> str:
        return self._value


class ObjectIDGenerator(IDGenerator[ObjectID]):
    """Bson ObjectId generator"""

    def unsafe_create_id(self) -> ObjectID:
        """Create a new ObjectId"""
        return ObjectID()

    def unsafe_revert(self) -> None:
        """ObjectIDGenerator does not decrement _inc in case of revert because counter
        all ObjectId share the same counter (regardless of module importing it).
        Users should NOT rely on the counter found in generated ObjectId"""
        pass


class NanoIDGenerator(IDGenerator[str]):
    """NanoID generator."""

    def __init__(
        self,
        alphabet: str = DEFAULT_ALPHABET,
        size: int = DEFAULT_SIZE,
    ) -> None:
        super().__init__()
        self._alphabet = alphabet
        self._size = size

    def unsafe_create_id(self) -> str:
        return nanoid(self._alphabet, self._size)


class NUIDGenerator(IDGenerator[bytearray]):
    def __init__(self) -> None:
        super().__init__()
        self._nuid = NUID()

    def unsafe_create_id(self) -> bytearray:
        return self._nuid.next()

    @staticmethod
    def id_to_string(value: bytearray) -> str:
        return value.decode()


class UUID1Generator(IDGenerator[UUID]):
    """UUID1 generator"""

    def unsafe_create_id(self) -> UUID:
        return uuid1()


class UUID4Generator(IDGenerator[UUID]):
    """UUID4 generator"""

    def unsafe_create_id(self) -> UUID:
        return uuid4()


class ULIDGenerator(IDGenerator[ULID]):
    """ULID generator"""

    def unsafe_create_id(self) -> ULID:
        return ULID()


class IncrementalIDGenerator(IDGenerator[int]):
    """Incremental integer generator"""

    def __init__(
        self, offset: t.Optional[int] = None, bound: t.Optional[int] = None
    ) -> None:
        super().__init__()
        self._inc = offset or 0
        self._bound = bound

    def unsafe_create_id(self) -> int:
        if self._bound and self._inc >= self._bound:
            self._inc = 0
        _id = self._inc
        self._inc += 1
        return _id

    def unsafe_revert(self) -> None:
        if self._inc:
            self._inc -= 1


class SecretIDGenerator(IDGenerator[str]):
    """Secret ID generator"""

    def __init__(self, length: int = 16) -> None:
        super().__init__()
        self._length = length

    def unsafe_create_id(self) -> str:
        return token_hex(self._length)


class TimestampGenerator(IDGenerator[int]):
    """Unix timestamp (seconds since unix epoch) generator"""

    def unsafe_create_id(self) -> int:
        return int(time())


class NanosecondTimestampGenerator(IDGenerator[int]):
    """Nanosecond timestamp generator"""

    def unsafe_create_id(self) -> int:
        return time_ns()


class Kind(str, enum.Enum):
    CONSTANT = "constant"
    NANOID = "nanoid"
    NUID = "nuid"
    OBJECTID = "objectid"
    UUID1 = "uuid1"
    UUID4 = "uuid4"
    ULID = "ulid"
    INCREMENTAL = "incremental"
    SECRET = "secret"
    TIMESTAMP = "timestamp"
    NSTIMESTAMP = "nstimestamp"


def generator(
    kind: t.Union[
        t.Literal[
            "constant",
            "nanoid",
            "objectid",
            "uuid1",
            "uuid4",
            "ulid",
            "incremental",
            "secret",
            "timestamp",
            "nstimestamp",
        ],
        Kind,
    ],
    **kwargs: t.Any,
) -> IDGenerator[t.Any]:
    """Create a new ID generator of specific kind.

    Supported kinds:

    - `"constant"`
    - `"nanoid"`
    - `"nuid"`
    - `"objectid"`
    - `"uuid1"`
    - `"uuid4"`
    - `"ulid"`
    - `"incremental"`
    - `"secret"`
    - `"timestamp"`
    - `"nstimestamp"`
    """
    # Validate kind
    kind = Kind(kind)
    if kind == Kind.CONSTANT:
        return ConstantIDGenerator(**kwargs)
    if kind == Kind.NANOID:
        return NanoIDGenerator(**kwargs)
    if kind == Kind.NUID:
        return NUIDGenerator(**kwargs)
    if kind == Kind.OBJECTID:
        return ObjectIDGenerator(**kwargs)
    if kind == Kind.UUID1:
        return UUID1Generator(**kwargs)
    if kind == Kind.UUID4:
        return UUID4Generator(**kwargs)
    if kind == Kind.ULID:
        return ULIDGenerator(**kwargs)
    if kind == Kind.INCREMENTAL:
        return IncrementalIDGenerator(**kwargs)
    if kind == Kind.SECRET:
        return SecretIDGenerator(**kwargs)
    if kind == Kind.TIMESTAMP:
        return TimestampGenerator(**kwargs)
    if kind == Kind.NSTIMESTAMP:
        return NanosecondTimestampGenerator(**kwargs)
    raise ValueError(f"Invalid ID kind: {kind}")
