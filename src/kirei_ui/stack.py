from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLayout, QLayoutItem, QVBoxLayout, QWidget
from typing_extensions import Self


class KireiHStack(QWidget):
    def __init__(self, *widgets: QWidget) -> None:
        super().__init__()
        self._layout = QHBoxLayout(self)
        for widget in widgets:
            self.add(widget)

    def add(self, widget: QWidget, stretch: int = 0) -> Self:
        self._layout.addWidget(widget, stretch)
        return self

    def add_layout(self, layout: QLayout, stretch: int = 0) -> Self:
        self._layout.addLayout(layout, stretch)
        return self

    def spacing(self, value: int) -> Self:
        self._layout.setSpacing(value)
        return self

    def padding(self, value: int) -> Self:
        self._layout.setContentsMargins(value, value, value, value)
        return self

    def margins(self, left: int, top: int, right: int, bottom: int) -> Self:
        self._layout.setContentsMargins(left, top, right, bottom)
        return self

    def stretch(self, value: int = 1) -> Self:
        self._layout.addStretch(value)
        return self

    def clear(self) -> Self:
        while self._layout.count() > 0:
            item = self._layout.takeAt(0)
            _clear_layout_item(item)
        return self

    def qt_layout(self) -> QHBoxLayout:
        return self._layout


class KireiVStack(QWidget):
    def __init__(self, *widgets: QWidget) -> None:
        super().__init__()
        self._layout = QVBoxLayout(self)
        for widget in widgets:
            self.add(widget)

    def add(self, widget: QWidget, stretch: int = 0) -> Self:
        self._layout.addWidget(widget, stretch)
        return self

    def add_layout(self, layout: QLayout, stretch: int = 0) -> Self:
        self._layout.addLayout(layout, stretch)
        return self

    def spacing(self, value: int) -> Self:
        self._layout.setSpacing(value)
        return self

    def padding(self, value: int) -> Self:
        self._layout.setContentsMargins(value, value, value, value)
        return self

    def margins(self, left: int, top: int, right: int, bottom: int) -> Self:
        self._layout.setContentsMargins(left, top, right, bottom)
        return self

    def stretch(self, value: int = 1) -> Self:
        self._layout.addStretch(value)
        return self

    def clear(self) -> Self:
        while self._layout.count() > 0:
            item = self._layout.takeAt(0)
            _clear_layout_item(item)
        return self

    def qt_layout(self) -> QVBoxLayout:
        return self._layout


def _clear_layout_item(item: QLayoutItem | None) -> None:
    if item is None:
        return
    widget = item.widget()
    if widget is not None:
        widget.setParent(None)
        return
    layout = item.layout()
    if layout is not None:
        while layout.count() > 0:
            child = layout.takeAt(0)
            _clear_layout_item(child)
