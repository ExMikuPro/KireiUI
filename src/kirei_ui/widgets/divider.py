from __future__ import annotations

from PySide6.QtWidgets import QFrame, QWidget
from typing_extensions import Self

from kirei_ui.utils import refresh_style


class KireiDivider(QFrame):
    """Thin separator line, horizontal by default.

    Wraps :class:`QFrame` with the line shape preset and KireiUI Qt
    properties (``kirei="divider"``, ``kireiRole="divider"``,
    ``kireiVariant="default"``). Switch orientation with
    :meth:`horizontal` / :meth:`vertical`; styling lives in QSS via
    the variant / role / objectName hooks.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "divider")
        self.setProperty("kireiRole", "divider")
        self.setProperty("kireiVariant", "default")
        self.horizontal()

    def horizontal(self) -> Self:
        """Render as a horizontal line (the default)."""
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(1)
        return self

    def vertical(self) -> Self:
        """Render as a vertical line (use inside an HBox)."""
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(1)
        return self

    def variant(self, name: str) -> Self:
        """Set the ``kireiVariant`` Qt property and re-polish QSS."""
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def spacing(self, value: int) -> Self:
        """Set uniform contents margins in pixels."""
        self.setContentsMargins(value, value, value, value)
        return self

    def object_name(self, name: str) -> Self:
        """Set ``QObject.objectName``, useful for ID-targeted QSS rules."""
        self.setObjectName(name)
        return self
