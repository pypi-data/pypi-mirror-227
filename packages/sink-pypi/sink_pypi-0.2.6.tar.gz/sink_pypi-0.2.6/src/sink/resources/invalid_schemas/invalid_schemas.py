# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

from .arrays import Arrays, AsyncArrays
from ..._resource import SyncAPIResource, AsyncAPIResource

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["InvalidSchemas", "AsyncInvalidSchemas"]


class InvalidSchemas(SyncAPIResource):
    arrays: Arrays

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.arrays = Arrays(client)


class AsyncInvalidSchemas(AsyncAPIResource):
    arrays: AsyncArrays

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.arrays = AsyncArrays(client)
