from types import TracebackType
from typing import Any, ContextManager, Generic, TypeVar


T = TypeVar("T", bound=ContextManager[Any])


class WithEnforcer(Generic[T]):
    """A wrapper class that enforces the usage of an object within a 'with' block context.

    **Allowed Attributes**
    * All attributes starting with '_'
    * prefix attributes with '_bypass_' \\
      ex) `_bypass_some_method()` will allow `some_method()` outside of 'with' block.

    Methods:
        __getattribute__(name: str) -> Any:
            Handles attribute access.
            1. Asserts that the object is within a 'with' block with boolean `_is_within`.
            2. Forwards attribute access to the wrapped object.

    Example:
        >>> cm: CM = WithEnforcer(some_context_manager) # type: ignore
        >>> with cm:
        >>>     cm.some_method()
        >>> cm.some_method()          # RuntimeError
        >>> cm._bypass_some_method()  # Success
    """

    _item: T

    def __init__(self, item: T):
        self._item = item
        self._is_within = False

    def __enter__(self):
        self._is_within = True
        self._item.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ):
        self._item.__exit__(exc_type, exc_value, traceback)
        self._is_within = False

    def _assert_within(self):
        if not self._is_within:
            raise RuntimeError(f"{self._item} can only be used within a 'with' block.")

    def __getattribute__(self, name: str):
        if name.startswith("_bypass_"):
            return getattr(
                object.__getattribute__(self, "_item"), name.removeprefix("_bypass_")
            )
        elif name.startswith("_"):
            # _item, _is_within, _assert_within belongs here
            return object.__getattribute__(self, name)
        else:
            self._assert_within()
            return getattr(object.__getattribute__(self, "_item"), name)
