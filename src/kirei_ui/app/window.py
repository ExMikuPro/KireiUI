from __future__ import annotations

from typing import overload

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from typing_extensions import Self


class KireiWindow(QMainWindow):
    """Base main window for KireiUI applications.

    Wraps :class:`QMainWindow` with a chainable API for the common
    setup steps: title, size, central content, and screen centering.
    The default size (1180x760) and title (``"KireiUI"``) match the
    examples in the docs.
    """

    def __init__(
        self,
        *,
        title: str = "KireiUI",
        width: int = 1180,
        height: int = 760,
        parent: QWidget | None = None,
    ) -> None:
        """Create the window.

        Args:
            title: Initial window title.
            width: Initial width in pixels.
            height: Initial height in pixels.
            parent: Parent widget (almost always ``None`` for a main window).
        """
        super().__init__(parent)

        self.setWindowTitle(title)
        self.resize(width, height)

    def set_content(self, widget: QWidget) -> None:
        """Set the main content widget. Non-chainable."""
        self.setCentralWidget(widget)

    def title(self, text: str) -> Self:
        """Set the window title. Chainable."""
        self.setWindowTitle(text)
        return self

    @overload
    def size(self) -> QSize: ...

    @overload
    def size(self, width: int, height: int) -> Self: ...

    def size(self, width: int | None = None, height: int | None = None) -> QSize | Self:
        """Get the current :class:`QSize` (no arg) or resize the window (chainable).

        Both ``width`` and ``height`` must be supplied together when
        setting; passing only one raises :class:`ValueError`.
        """
        if width is None and height is None:
            return super().size()
        if width is None or height is None:
            raise ValueError("Both width and height are required.")
        self.resize(width, height)
        return self

    def content(self, widget: QWidget) -> Self:
        """Chainable :meth:`set_content`."""
        self.set_content(widget)
        return self

    def fixed_size(self, width: int, height: int) -> Self:
        """Lock the window to the given size — user can't resize."""
        self.setFixedSize(width, height)
        return self

    def min_size(self, width: int, height: int) -> Self:
        """Set the minimum size (user-resizable above this)."""
        self.setMinimumSize(width, height)
        return self

    def max_size(self, width: int, height: int) -> Self:
        """Set the maximum size (user-resizable up to this)."""
        self.setMaximumSize(width, height)
        return self

    def center(self) -> Self:
        """Move the window to the center of the primary screen.

        Silently no-ops when no :class:`QApplication` instance is
        running or the primary screen cannot be determined.
        """
        app = QApplication.instance()
        if not isinstance(app, QApplication):
            return self
        screen = app.primaryScreen()
        if screen is None:
            return self
        frame = self.frameGeometry()
        frame.moveCenter(screen.availableGeometry().center())
        self.move(frame.topLeft())
        return self

    def set_placeholder(self, text: str = "Hello KireiUI") -> None:
        """Set a simple centered placeholder label as the central widget.

        Useful for the very first run-through of an example before any
        real content widget exists.
        """
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("KireiWindowPlaceholder")

        self.setCentralWidget(label)
