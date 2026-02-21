from abc import ABC, abstractmethod
from typing import Tuple


class Backend(ABC):
    """Abstract base class for pick UI backends."""

    @abstractmethod
    def setup(self) -> None: ...

    @abstractmethod
    def teardown(self) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...

    @abstractmethod
    def getmaxyx(self) -> Tuple[int, int]: ...

    @abstractmethod
    def addnstr(self, y: int, x: int, s: str, n: int) -> None: ...

    @abstractmethod
    def getch(self) -> int: ...

    @abstractmethod
    def refresh(self) -> None: ...
