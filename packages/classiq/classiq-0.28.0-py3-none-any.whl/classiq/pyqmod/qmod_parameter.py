from typing import Any, Generic, TypeVar

from sympy import Symbol
from sympy.core.compatibility import NotIterable

_T = TypeVar("_T")


class QParam(Symbol, NotIterable, Generic[_T]):
    def __getitem__(self, key: Any) -> "QParam":
        return QParam(name=f"{str(self)}[{str(key)}]")
