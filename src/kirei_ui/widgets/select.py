from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from PySide6.QtWidgets import QComboBox, QWidget
from typing_extensions import Self

from kirei_ui.utils import keep_callback


class KireiComboBox(QComboBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "combobox")
        self.setProperty("kireiRole", "combobox")

    def add_item(self, text: str, data: object | None = None) -> Self:
        self.addItem(text, userData=data)
        return self

    def add_items(self, items: Iterable[str]) -> Self:
        self.addItems(list(items))
        return self

    def current(self, value: str) -> Self:
        index = self.findText(value)
        if index >= 0:
            self.setCurrentIndex(index)
        return self

    def current_index(self, index: int) -> Self:
        self.setCurrentIndex(index)
        return self

    def get_value(self) -> str:
        return self.currentText()

    def get_data(self) -> Any:
        return self.currentData()

    def on_change(self, callback: Callable[[str], object]) -> Self:
        handler = keep_callback(self, callback)
        self.currentTextChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self
