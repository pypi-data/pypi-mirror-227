from __future__ import annotations

import sys
from typing import Any
from typing import TYPE_CHECKING

import inkex

from . import typing as types

__all__ = [
    "compose_transforms",
    "ensure_str",
    "to_dimensionless",
    "Literal",
    "TypedDict",
]

if sys.version_info >= (3, 8):
    from typing import Literal
    from typing import TypedDict
elif TYPE_CHECKING:
    from typing_extensions import Literal
    from typing_extensions import TypedDict
else:

    class LiteralType:
        def __getitem__(self, _key: Any) -> LiteralType:
            return self

    Literal = LiteralType()

    class TypedDict:
        def __init_subclass__(cls, total: bool = True, **kwargs: Any) -> None:
            super().__init_subclass__(**kwargs)


def ensure_str(s: bytes | str, encoding: str = "utf-8", errors: str = "strict") -> str:
    """Coerce bytes to str."""
    if isinstance(s, bytes):
        return s.decode(encoding, errors=errors)
    return s


if hasattr(inkex.Transform, "__matmul__"):

    def compose_transforms(
        x: types.TransformLike, y: types.TransformLike
    ) -> inkex.Transform:
        """Compose two inkex.Transforms.

        This version works with Inkscape version 1.2 and above.
        """
        return inkex.Transform(x) @ y

else:

    def compose_transforms(
        x: types.TransformLike, y: types.TransformLike
    ) -> inkex.Transform:
        """Compose two inkex.Transforms.

        This version works with Inkscapes before version 1.2 whose
        Transforms do not support __matmul__.
        """
        return inkex.Transform(x) * y


if hasattr(inkex.BaseElement, "to_dimensionless"):

    def to_dimensionless(elem: inkex.BaseElement, value: str) -> float:
        """Convert length to dimensionless user units (px)

        This version works with Inkscape version 1.2 and above.
        """
        return elem.to_dimensionless(value)  # type: ignore[no-any-return]

else:

    def to_dimensionless(
        elem: inkex.BaseElement,  # pylint: disable=unused-argument
        value: str,
    ) -> float:
        """Convert length to dimensionless user units (px)

        This version works with Inkscape versions below 1.2.
        """
        return inkex.units.convert_unit(value, "px")  # type: ignore[no-any-return]
