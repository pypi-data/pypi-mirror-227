# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["TypeEnumsParams"]


class TypeEnumsParams(TypedDict, total=False):
    input_currency: Optional[
        Literal["USD", "GBP", "PAB", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM"]
    ]
    """This is my description for the Currency enum"""

    problematic_enum: Literal["123_FOO", "30%"]
