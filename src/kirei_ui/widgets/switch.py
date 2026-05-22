from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QCheckBox, QWidget
from typing_extensions import Self

from kirei_ui.utils import keep_callback, refresh_style


class KireiSwitch(QCheckBox):
    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kirei", "switch")
        self.setProperty("kireiRole", "switch")
        self.setProperty("kireiVariant", "default")
        self.setProperty("kireiSize", "default")

    def text(self, value: str) -> Self:
        self.setText(value)
        return self

    def checked(self, value: bool = True) -> Self:
        self.setChecked(value)
        return self

    def is_checked(self) -> bool:
        return self.isChecked()

    def on_change(self, callback: Callable[[bool], object]) -> Self:
        handler = keep_callback(self, callback)
        self.toggled.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self

    def variant(self, name: str) -> Self:
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def size(self, name: str) -> Self:
        self.setProperty("kireiSize", name)
        refresh_style(self)
        return self
