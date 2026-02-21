import contextlib
import curses
from typing import Optional, Tuple

from .backend import Backend


class BlessedBackend(Backend):
    """Backend that uses the blessed library (optional dependency)."""

    def __init__(self) -> None:
        try:
            import blessed
        except ImportError:
            raise ImportError(
                "blessed is required for BlessedBackend. "
                "Install with: pip install pick[blessed]"
            )
        self._term = blessed.Terminal()
        self._ctx: Optional[contextlib.ExitStack] = None

    def setup(self) -> None:
        self._ctx = contextlib.ExitStack()
        self._ctx.enter_context(self._term.fullscreen())
        self._ctx.enter_context(self._term.cbreak())
        self._ctx.enter_context(self._term.hidden_cursor())

    def teardown(self) -> None:
        if self._ctx is not None:
            self._ctx.close()
            self._ctx = None

    def clear(self) -> None:
        print(self._term.home + self._term.clear, end='', flush=True)

    def getmaxyx(self) -> Tuple[int, int]:
        return (self._term.height, self._term.width)

    def addnstr(self, y: int, x: int, s: str, n: int) -> None:
        print(self._term.move_yx(y, x) + s[:n], end='', flush=True)

    def getch(self) -> int:
        key = self._term.inkey()
        if key.is_sequence:
            mapping = {
                'KEY_UP': curses.KEY_UP,
                'KEY_DOWN': curses.KEY_DOWN,
                'KEY_RIGHT': curses.KEY_RIGHT,
                'KEY_ENTER': curses.KEY_ENTER,
            }
            return mapping.get(key.name, -1)
        return ord(key) if key else -1

    def refresh(self) -> None:
        pass  # blessed prints directly, no refresh needed
