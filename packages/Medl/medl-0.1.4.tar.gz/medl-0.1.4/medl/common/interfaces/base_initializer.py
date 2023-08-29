from typing import Protocol

__all__ = ["BaseInitializer"]


class BaseInitializer(Protocol):
    def init(self) -> None:
        ...
