from __future__ import annotations

from typing import overload

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from typing_extensions import Self


class KireiWindow(QMainWindow):
    """Base main window for KireiUI applications."""

    def __init__(
        self,
        *,
        title: str = "KireiUI",
        width: int = 1180,
        height: int = 760,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(title)
        self.resize(width, height)

    def set_content(self, widget: QWidget) -> None:
        """Set the main content widget."""
        self.setCentralWidget(widget)

    def title(self, text: str) -> Self:
        self.setWindowTitle(text)
        return self

    @overload
    def size(self) -> QSize: ...

    @overload
    def size(self, width: int, height: int) -> Self: ...

    def size(self, width: int | None = None, height: int | None = None) -> QSize | Self:
        if width is None and height is None:
            return super().size()
        if width is None or height is None:
            raise ValueError("Both width and height are required.")
        self.resize(width, height)
        return self

    def content(self, widget: QWidget) -> Self:
        self.set_content(widget)
        return self

    def fixed_size(self, width: int, height: int) -> Self:
        self.setFixedSize(width, height)
        return self

    def min_size(self, width: int, height: int) -> Self:
        self.setMinimumSize(width, height)
        return self

    def max_size(self, width: int, height: int) -> Self:
        self.setMaximumSize(width, height)
        return self

    def center(self) -> Self:
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
        """Set a simple placeholder label as the central widget."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("KireiWindowPlaceholder")

        self.setCentralWidget(label)
