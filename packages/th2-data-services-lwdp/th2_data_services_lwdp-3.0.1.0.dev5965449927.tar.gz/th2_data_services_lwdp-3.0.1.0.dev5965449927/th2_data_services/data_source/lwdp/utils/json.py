#  Copyright 2023 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from typing import Generator

import orjson as json
from orjson import JSONDecodeError


class BufferedJSONProcessor:
    def __init__(self, buffer_limit: int = 250):
        """BufferedJSONProcessor constructor.

        Args:
            buffer_limit: By default 250. If limit is 0 buffer will not be used.
        """
        self.buffer = []
        self.buffer_limit = buffer_limit
        if buffer_limit == 0:
            self.decode = self._decode_without_buffer
        else:
            self.decode = self._decode_with_buffer

    def from_buffer(self) -> Generator:
        """Transforms JSON objects to dict objects.

        Returns:
            Generator[dict]
        """
        try:
            for i in json.loads("[" + ",".join(self.buffer) + "]"):
                yield i
        except JSONDecodeError as e:
            raise ValueError(
                f"json.decoder.JSONDecodeError: Invalid json received.\n" f"{e}\n" f"{self.buffer}"
            )
        finally:
            # Prevents StopIteration issues
            self.buffer = []

    def _decode_without_buffer(self, x: str) -> dict:
        """Decode JSON without buffer.

        Args:
            x: JSON Object

        Returns:
            dict
        """
        yield json.loads(x)

    def _decode_with_buffer(self, x: str) -> dict:
        """Decode JSON with buffer.

        Args:
            x: JSON Object

        Returns:
            dict
        """
        if len(self.buffer) < self.buffer_limit:
            self.buffer.append(x)
        else:
            yield from self.from_buffer()
            self.buffer = [x]

    def fin(self) -> Generator:
        """If buffer exists returns dicts from buffer.

        Returns:
            Generator[dict]
        """
        if self.buffer:
            yield from self.from_buffer()
