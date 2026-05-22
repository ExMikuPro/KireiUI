from __future__ import annotations

from collections.abc import Callable, Iterable

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)
from typing_extensions import Self

from kirei_ui.utils import clear_layout, keep_callback
from kirei_ui.widgets.input import KireiInput


class KireiTable(QTableWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "table")
        self.setProperty("kireiRole", "table")

    def columns(self, headers: list[str]) -> Self:
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        return self

    def rows(self, values: list[list[object]]) -> Self:
        self.setRowCount(0)
        for row in values:
            self.add_row(row)
        return self

    def add_row(self, values: list[object]) -> Self:
        row = self.rowCount()
        self.insertRow(row)
        for col, value in enumerate(values):
            self.setItem(row, col, QTableWidgetItem(str(value)))
        return self

    def clear_rows(self) -> Self:
        self.setRowCount(0)
        return self

    def selected_row(self) -> int:
        return self.currentRow()

    def on_cell_click(self, callback: Callable[[int, int], object]) -> Self:
        self.cellClicked.connect(keep_callback(self, callback))
        return self


class KireiList(QListWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "list")
        self.setProperty("kireiRole", "list")

    def add_item(self, text: str, data: object | None = None) -> Self:
        item = QListWidgetItem(text)
        if data is not None:
            item.setData(0x0100, data)
        self.addItem(item)
        return self

    def add_items(self, items: Iterable[str]) -> Self:
        for text in items:
            self.add_item(text)
        return self

    def current(self, value: str) -> Self:
        for i in range(self.count()):
            item = self.item(i)
            if item is not None and item.text() == value:
                self.setCurrentRow(i)
                break
        return self

    def get_value(self) -> str:
        item = self.currentItem()
        return "" if item is None else item.text()

    def on_change(self, callback: Callable[[str], object]) -> Self:
        def handler(item: QListWidgetItem | None) -> object:
            return callback("" if item is None else item.text())

        self.currentItemChanged.connect(keep_callback(self, handler))
        return self


class KireiTree(QTreeWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "tree")
        self.setProperty("kireiRole", "tree")

    def headers(self, values: list[str]) -> Self:
        self.setColumnCount(len(values))
        self.setHeaderLabels(values)
        return self

    def add_item(self, values: list[str]) -> Self:
        self.addTopLevelItem(QTreeWidgetItem(values))
        return self

    def clear_items(self) -> Self:
        self.clear()
        return self


class KireiSearchBox(KireiInput):
    def __init__(self, value: str = "", parent: QWidget | None = None) -> None:
        super().__init__(value=value, parent=parent)
        self.setProperty("kireiRole", "searchBox")

    def on_search(self, callback: Callable[[str], object]) -> Self:
        def handler() -> object:
            return callback(self.get_value())

        self.returnPressed.connect(keep_callback(self, handler))
        return self


class KireiFilterBar(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "filter-bar")
        self.setProperty("kireiRole", "filterBar")
        self._filters = QHBoxLayout()
        self._actions = QHBoxLayout()

        layout = QHBoxLayout(self)
        layout.addLayout(self._filters)
        layout.addStretch(1)
        layout.addLayout(self._actions)

    def add_filter(self, widget: QWidget) -> Self:
        self._filters.addWidget(widget)
        return self

    def add_action(self, widget: QWidget) -> Self:
        self._actions.addWidget(widget)
        return self

    def clear_filters(self) -> Self:
        clear_layout(self._filters)
        return self


class KireiPagination(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "pagination")
        self.setProperty("kireiRole", "pagination")
        self._total = 0
        self._page = 1
        self._page_size = 10

        self._label = QLabel("")
        self._prev = QPushButton("Prev")
        self._next = QPushButton("Next")
        self._prev.clicked.connect(self._prev_page)
        self._next.clicked.connect(self._next_page)

        layout = QHBoxLayout(self)
        layout.addWidget(self._prev)
        layout.addWidget(self._next)
        layout.addWidget(self._label)
        layout.addStretch(1)
        self._render()

    def total(self, value: int) -> Self:
        self._total = max(0, value)
        self._render()
        return self

    def page(self, value: int) -> Self:
        self._page = max(1, value)
        self._render()
        return self

    def page_size(self, value: int) -> Self:
        self._page_size = max(1, value)
        self._render()
        return self

    def on_change(self, callback: Callable[[int], object]) -> Self:
        keep_callback(self, callback)
        return self

    def _emit_change(self) -> None:
        for callback in getattr(self, "_kirei_callbacks", []):
            callback(self._page)

    def _prev_page(self) -> None:
        if self._page > 1:
            self._page -= 1
            self._render()
            self._emit_change()

    def _next_page(self) -> None:
        max_page = max(1, (self._total + self._page_size - 1) // self._page_size)
        if self._page < max_page:
            self._page += 1
            self._render()
            self._emit_change()

    def _render(self) -> None:
        max_page = max(1, (self._total + self._page_size - 1) // self._page_size)
        if self._page > max_page:
            self._page = max_page
        self._label.setText(f"Page {self._page}/{max_page} · Total {self._total}")
