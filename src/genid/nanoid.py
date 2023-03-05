# Copyright (c) 2018 Paul Yuan
# Copyright (c) 2018 Dair Aidarkhanov
# Copyright (c) 2018 Andrey Sitnik <andrey@sitnik.ru>
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
"""Taken from https://github.com/puyuan/py-nanoid"""
import string
from math import ceil, log
from secrets import token_hex

# Using default alphabet and default size
# Assuming one id is generated every second
# ~41 billion years needed in order to have a 1% probability of at least one collision
DEFAULT_ALPHABET = f"_-{string.digits}{string.ascii_letters}"
DEFAULT_SIZE = 21
LOG2 = log(2)


def nanoid(alphabet: str = DEFAULT_ALPHABET, size: int = DEFAULT_SIZE) -> str:
    """Implementation taken from https://github.com/puyuan/py-nanoid

    This is functionally equivalent to calling secrets.choice(alphabet) until generated string
    is of desired size, but it is 10~15x faster than calling secrets.choice.
    """
    alphabet_len = len(alphabet)

    mask = 1
    if alphabet_len > 1:
        mask = (2 << int(log(alphabet_len - 1) / LOG2)) - 1
    step = int(ceil(1.6 * mask * size / alphabet_len))

    _id = ""
    while True:
        random_bytes = token_hex(step).encode()

        for i in range(step):
            random_byte = random_bytes[i] & mask
            if random_byte < alphabet_len and alphabet[random_byte]:
                _id += alphabet[random_byte]

                if len(_id) == size:
                    return _id
