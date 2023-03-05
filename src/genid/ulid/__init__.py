# Copyright (c) 2017 Martin Domke
# Modifications copyright (c) 2023 Guillaume Charbonnier
#
# Licensed under the MIT license;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://mit-license.org/
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Taken from https://python-ulid.readthedocs.io/en/latest/"""

import functools
import os
import time
import typing as t
import uuid
from datetime import datetime, timezone

from . import base32, constants


@functools.total_ordering
class ULID:
    """The :class:`ULID` object consists of a timestamp part of 48 bits and of 80 random bits.

    .. code-block:: text

       01AN4Z07BY      79KA1307SR9X4MV3
      |----------|    |----------------|
       Timestamp          Randomness
         48bits             80bits

    You usually create a new :class:`ULID`-object by calling the default constructor with now
    arguments. In that case it will fill the timestamp part with the current datetime. To encode the
    object you usually convert it to a string:

        >>> ulid = ULID()
        >>> str(ulid)
        '01E75PVKXA3GFABX1M1J9NZZNF'
    """

    def __init__(self, value: t.Optional[bytes] = None) -> None:
        if value is not None and len(value) != constants.BYTES_LEN:
            raise ValueError("ULID has to be exactly 16 bytes long.")
        if value:
            self.bytes = value
        else:
            _id = ULID.from_timestamp(time.time())
            self.bytes = _id.bytes

    @classmethod
    def from_datetime(cls, value: datetime) -> "ULID":
        """Create a new :class:`ULID`-object from a :class:`datetime`. The timestamp part of the
        `ULID` will be set to the corresponding timestamp of the datetime.

        Examples:

            >>> from datetime import datetime
            >>> ULID.from_datetime(datetime.now())
            ULID(01E75QRYCAMM1MKQ9NYMYT6SAV)
        """
        return cls.from_timestamp(value.timestamp())

    @classmethod
    def from_timestamp(cls, value: t.Union[int, float]) -> "ULID":
        """Create a new :class:`ULID`-object from a timestamp. The timestamp can be either a
        `float` representing the time in seconds (as it would be returned by :func:`time.time()`)
        or an `int` in milliseconds.

        Examples:

            >>> import time
            >>> ULID.from_timestamp(time.time())
            ULID(01E75QWN5HKQ0JAVX9FG1K4YP4)
        """
        if isinstance(value, float):
            value = int(value * constants.MILLISECS_IN_SECS)
        if isinstance(value, int):
            timestamp = int.to_bytes(value, constants.TIMESTAMP_LEN, "big")
            randomness = os.urandom(constants.RANDOMNESS_LEN)
            return cls.from_bytes(timestamp + randomness)
        raise TypeError(f"Exepected int or float value, not {type(value)}")

    @classmethod
    def from_uuid(cls, value: uuid.UUID) -> "ULID":
        """Create a new :class:`ULID`-object from a :class:`uuid.UUID`. The timestamp part will be
        random in that case.

        Examples:

            >>> from uuid import uuid4
            >>> ULID.from_uuid(uuid4())
            ULID(27Q506DP7E9YNRXA0XVD8Z5YSG)
        """
        if isinstance(value, uuid.UUID):
            return cls(value.bytes)
        raise TypeError(f"Expected UUID value, not {type(value)}")

    @classmethod
    def from_bytes(cls, value: bytes) -> "ULID":
        """Create a new :class:`ULID`-object from sequence of 16 bytes."""
        if isinstance(value, bytes):
            return cls(value)
        raise TypeError(f"Expected bytes value, not {type(value)}")

    @classmethod
    def from_hex(cls, value: str) -> "ULID":
        """Create a new :class:`ULID`-object from 32 character string of hex values."""
        if isinstance(value, str):
            return cls.from_bytes(bytes.fromhex(value))
        raise TypeError(f"Expected str value, not {type(value)}")

    @classmethod
    def from_str(cls, value: str) -> "ULID":
        """Create a new :class:`ULID`-object from a 26 char long string representation."""
        if isinstance(value, str):
            return cls(base32.decode(value))
        raise TypeError(f"Expected str value, not {type(value)}")

    @classmethod
    def from_int(cls, value: int) -> "ULID":
        """Create a new :class:`ULID`-object from an `int`."""
        if isinstance(value, int):
            return cls(int.to_bytes(value, constants.BYTES_LEN, "big"))
        raise TypeError(f"Expected int value, not {type(value)}")

    @property
    def milliseconds(self) -> int:
        """The timestamp part as epoch time in milliseconds.

        Examples:

            >>> ulid.timestamp
            1588257207560
        """
        return int.from_bytes(self.bytes[: constants.TIMESTAMP_LEN], byteorder="big")

    @property
    def timestamp(self) -> float:
        """The timestamp part as epoch time in seconds.

        Examples:

            >>> ulid.timestamp
            1588257207.56
        """
        return self.milliseconds / constants.MILLISECS_IN_SECS

    @property
    def datetime(self) -> datetime:
        """Return the timestamp part as timezone-aware :class:`datetime` in UTC.

        Examples:

            >>> ulid.datetime
            datetime.datetime(2020, 4, 30, 14, 33, 27, 560000, tzinfo=datetime.timezone.utc)
        """
        return datetime.fromtimestamp(self.timestamp, timezone.utc)

    @property
    def hex(self) -> str:
        """Encode the :class:`ULID`-object as a 32 char sequence of hex values."""
        return self.bytes.hex()

    def to_uuid(self) -> uuid.UUID:
        """Convert the :class:`ULID` to a :class:`uuid.UUID`."""
        return uuid.UUID(bytes=self.bytes)

    def __repr__(self) -> str:
        return f"ULID({self!s})"

    def __str__(self) -> str:
        """Encode this object as a 26 character string sequence."""
        return base32.encode(self.bytes)

    def __int__(self) -> int:
        """Encode this object as an integer."""
        return int.from_bytes(self.bytes, byteorder="big")

    def __lt__(self, other: t.Any) -> bool:
        if isinstance(other, ULID):
            return self.bytes < other.bytes
        elif isinstance(other, int):
            return int(self) < other
        elif isinstance(other, bytes):
            return self.bytes < other
        elif isinstance(other, str):
            return str(self) < other
        return NotImplemented

    def __eq__(self, other: t.Any) -> bool:
        if isinstance(other, ULID):
            return self.bytes == other.bytes
        elif isinstance(other, int):
            return int(self) == other
        elif isinstance(other, bytes):
            return self.bytes == other
        elif isinstance(other, str):
            return str(self) == other
        return NotImplemented
