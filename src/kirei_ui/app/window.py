from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QWidget


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

    def set_placeholder(self, text: str = "Hello KireiUI") -> None:
        """Set a simple placeholder label as the central widget."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("KireiWindowPlaceholder")

        self.setCentralWidget(label)
