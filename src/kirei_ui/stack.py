from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLayout,
    QLayoutItem,
    QScrollArea,
    QSplitter,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
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
        _clear_layout(self._layout)
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
        _clear_layout(self._layout)
        return self

    def qt_layout(self) -> QVBoxLayout:
        return self._layout


class KireiGrid(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QGridLayout(self)

    def add_at(
        self,
        widget: QWidget,
        row: int,
        column: int,
        row_span: int = 1,
        column_span: int = 1,
    ) -> Self:
        self._layout.addWidget(widget, row, column, row_span, column_span)
        return self

    def spacing(self, value: int) -> Self:
        self._layout.setSpacing(value)
        return self

    def horizontal_spacing(self, value: int) -> Self:
        self._layout.setHorizontalSpacing(value)
        return self

    def vertical_spacing(self, value: int) -> Self:
        self._layout.setVerticalSpacing(value)
        return self

    def padding(self, value: int) -> Self:
        self._layout.setContentsMargins(value, value, value, value)
        return self

    def margins(self, left: int, top: int, right: int, bottom: int) -> Self:
        self._layout.setContentsMargins(left, top, right, bottom)
        return self

    def clear(self) -> Self:
        _clear_layout(self._layout)
        return self

    def qt_layout(self) -> QGridLayout:
        return self._layout


class KireiForm(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QFormLayout(self)

    def add_row(self, label: str | QWidget, field: QWidget) -> Self:
        self._layout.addRow(label, field)
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

    def clear(self) -> Self:
        _clear_layout(self._layout)
        return self

    def qt_layout(self) -> QFormLayout:
        return self._layout


class KireiScroll(QScrollArea):
    def content(self, widget: QWidget) -> Self:
        self.setWidget(widget)
        return self

    def resizable(self, value: bool = True) -> Self:
        self.setWidgetResizable(value)
        return self

    def horizontal_policy(self, policy: Qt.ScrollBarPolicy) -> Self:
        self.setHorizontalScrollBarPolicy(policy)
        return self

    def vertical_policy(self, policy: Qt.ScrollBarPolicy) -> Self:
        self.setVerticalScrollBarPolicy(policy)
        return self


class KireiPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self._content_layout = QVBoxLayout(self)

    def content(self, widget: QWidget) -> Self:
        _clear_layout(self._content_layout)
        self._content_layout.addWidget(widget)
        return self

    def padding(self, value: int) -> Self:
        self._content_layout.setContentsMargins(value, value, value, value)
        return self

    def margins(self, left: int, top: int, right: int, bottom: int) -> Self:
        self._content_layout.setContentsMargins(left, top, right, bottom)
        return self

    def variant(self, name: str) -> Self:
        self.setProperty("variant", name)
        return self

    def object_name(self, name: str) -> Self:
        self.setObjectName(name)
        return self


class KireiSplitter(QSplitter):
    @classmethod
    def horizontal(cls) -> Self:
        return cls(Qt.Orientation.Horizontal)

    @classmethod
    def vertical(cls) -> Self:
        return cls(Qt.Orientation.Vertical)

    def add(self, widget: QWidget) -> Self:
        self.addWidget(widget)
        return self

    def sizes(self, values: list[int]) -> Self:
        self.setSizes(values)
        return self


class KireiStack(QStackedWidget):
    def __init__(self) -> None:
        super().__init__()
        self._pages: dict[str, QWidget] = {}

    def add_page(self, name: str, widget: QWidget) -> Self:
        self._pages[name] = widget
        self.addWidget(widget)
        return self

    def current(self, name: str) -> Self:
        widget = self._pages.get(name)
        if widget is not None:
            self.setCurrentWidget(widget)
        return self

    def current_index(self, index: int) -> Self:
        self.setCurrentIndex(index)
        return self

    def page(self, name: str) -> QWidget | None:
        return self._pages.get(name)


class KireiTabs(QTabWidget):
    def add_tab(self, title: str, widget: QWidget) -> Self:
        self.addTab(widget, title)
        return self

    def current_index(self, index: int) -> Self:
        self.setCurrentIndex(index)
        return self

    def tabs_closable(self, value: bool = True) -> Self:
        self.setTabsClosable(value)
        return self


def _clear_layout(layout: QLayout) -> None:
    while layout.count() > 0:
        item = layout.takeAt(0)
        _clear_layout_item(item)


def _clear_layout_item(item: QLayoutItem | None) -> None:
    if item is None:
        return
    widget = item.widget()
    if widget is not None:
        widget.setParent(None)
        return
    child_layout = item.layout()
    if child_layout is not None:
        _clear_layout(child_layout)
