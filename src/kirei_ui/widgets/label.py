from __future__ import annotations

from typing import overload

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget
from typing_extensions import Self

from kirei_ui.utils import refresh_style


class KireiLabel(QLabel):
    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kirei", "label")
        self.setProperty("kireiRole", "label")

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def align_center(self) -> Self:
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return self

    def align_left(self) -> Self:
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return self

    def align_right(self) -> Self:
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return self

    def word_wrap(self, value: bool = True) -> Self:
        self.setWordWrap(value)
        return self

    def variant(self, name: str) -> Self:
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def role(self, name: str) -> Self:
        self.setProperty("kireiRole", name)
        refresh_style(self)
        return self

    def object_name(self, name: str) -> Self:
        self.setObjectName(name)
        return self

    def tooltip(self, value: str) -> Self:
        self.setToolTip(value)
        return self


class KireiTitle(KireiLabel):
    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kireiRole", "title")


class KireiText(KireiLabel):
    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kireiRole", "text")
