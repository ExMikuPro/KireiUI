from __future__ import annotations

from PySide6.QtWidgets import QFrame, QWidget
from typing_extensions import Self


class KireiDivider(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "divider")
        self.setProperty("kireiRole", "divider")
        self.setProperty("kireiVariant", "default")
        self.horizontal()

    def horizontal(self) -> Self:
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(1)
        return self

    def vertical(self) -> Self:
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(1)
        return self

    def variant(self, name: str) -> Self:
        self.setProperty("kireiVariant", name)
        self._refresh_style()
        return self

    def spacing(self, value: int) -> Self:
        self.setContentsMargins(value, value, value, value)
        return self

    def object_name(self, name: str) -> Self:
        self.setObjectName(name)
        return self

    def _refresh_style(self) -> None:
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
