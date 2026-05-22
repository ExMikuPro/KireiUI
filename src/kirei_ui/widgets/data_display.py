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
    """Simple tabular data widget with the KireiUI fluent API.

    Wraps :class:`QTableWidget` for the common case of plain string
    cells. Use :meth:`columns` to set headers, :meth:`rows` to replace
    all rows in one call, and :meth:`add_row` to append. Cells are
    coerced to ``str`` — provide pre-formatted values.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "table")
        self.setProperty("kireiRole", "table")

    def columns(self, headers: list[str]) -> Self:
        """Set the column headers and (re-)allocate column count."""
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        return self

    def rows(self, values: list[list[object]]) -> Self:
        """Replace all rows with ``values`` (each inner list is one row)."""
        self.setRowCount(0)
        for row in values:
            self.add_row(row)
        return self

    def add_row(self, values: list[object]) -> Self:
        """Append a single row. Each cell value is rendered via ``str(value)``."""
        row = self.rowCount()
        self.insertRow(row)
        for col, value in enumerate(values):
            self.setItem(row, col, QTableWidgetItem(str(value)))
        return self

    def clear_rows(self) -> Self:
        """Drop every row, keeping the headers and column count."""
        self.setRowCount(0)
        return self

    def selected_row(self) -> int:
        """Return the row index of the active cell (``-1`` if none)."""
        return self.currentRow()

    def on_cell_click(self, callback: Callable[[int, int], object]) -> Self:
        """Fire when a cell is clicked. Receives ``(row, column)``."""
        self.cellClicked.connect(keep_callback(self, callback))
        return self


class KireiList(QListWidget):
    """Vertical list of selectable string items.

    Wraps :class:`QListWidget`. Items can carry a hidden payload via
    Qt's user-role data (read it back with the standard
    :meth:`QListWidgetItem.data` API). :meth:`on_change` reports the
    new selection's display text.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "list")
        self.setProperty("kireiRole", "list")

    def add_item(self, text: str, data: object | None = None) -> Self:
        """Append a single entry. ``data`` is stored on Qt's user role."""
        item = QListWidgetItem(text)
        if data is not None:
            item.setData(0x0100, data)
        self.addItem(item)
        return self

    def add_items(self, items: Iterable[str]) -> Self:
        """Append multiple text-only entries in one call."""
        for text in items:
            self.add_item(text)
        return self

    def current(self, value: str) -> Self:
        """Select the first item whose text equals ``value`` (no-op if missing)."""
        for i in range(self.count()):
            item = self.item(i)
            if item is not None and item.text() == value:
                self.setCurrentRow(i)
                break
        return self

    def get_value(self) -> str:
        """Return the selected item's text, or ``""`` if nothing is selected."""
        item = self.currentItem()
        return "" if item is None else item.text()

    def on_change(self, callback: Callable[[str], object]) -> Self:
        """Fire when the selection changes. Receives the new item's text."""
        def handler(item: QListWidgetItem | None) -> object:
            return callback("" if item is None else item.text())

        self.currentItemChanged.connect(keep_callback(self, handler))
        return self


class KireiTree(QTreeWidget):
    """Tree view with the KireiUI fluent API.

    Wraps :class:`QTreeWidget`. Currently exposes top-level row
    operations only — use the underlying :class:`QTreeWidget` API for
    nested children.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "tree")
        self.setProperty("kireiRole", "tree")

    def headers(self, values: list[str]) -> Self:
        """Set column headers and (re-)allocate column count."""
        self.setColumnCount(len(values))
        self.setHeaderLabels(values)
        return self

    def add_item(self, values: list[str]) -> Self:
        """Append a top-level row. Values map column-by-column."""
        self.addTopLevelItem(QTreeWidgetItem(values))
        return self

    def clear_items(self) -> Self:
        """Drop every row, keeping the headers."""
        self.clear()
        return self


class KireiSearchBox(KireiInput):
    """Single-line search input with an Enter-to-search hook.

    Inherits the chainable API of :class:`KireiInput` and overrides
    ``kireiRole`` to ``"searchBox"``. Use :meth:`on_search` to react
    when the user presses Enter; the callback receives the current
    text rather than a Qt event.
    """

    def __init__(self, value: str = "", parent: QWidget | None = None) -> None:
        super().__init__(value=value, parent=parent)
        self.setProperty("kireiRole", "searchBox")

    def on_search(self, callback: Callable[[str], object]) -> Self:
        """Fire on Enter / Return. Receives the current text."""
        def handler() -> object:
            return callback(self.get_value())

        self.returnPressed.connect(keep_callback(self, handler))
        return self


class KireiFilterBar(QWidget):
    """Horizontal toolbar with leading filter widgets and trailing actions.

    Two regions arranged left-to-right with a stretch in the middle.
    Use :meth:`add_filter` for filter controls (combos, search,
    chips), :meth:`add_action` for trailing buttons. Filters can be
    reset with :meth:`clear_filters`; actions persist.
    """

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
        """Append a control to the leading (left) filter region."""
        self._filters.addWidget(widget)
        return self

    def add_action(self, widget: QWidget) -> Self:
        """Append a control to the trailing (right) action region."""
        self._actions.addWidget(widget)
        return self

    def clear_filters(self) -> Self:
        """Detach every widget in the leading filter region. Actions are kept."""
        clear_layout(self._filters)
        return self


class KireiPagination(QWidget):
    """Prev / Next pagination control with page-state callbacks.

    Tracks ``total``, ``page`` and ``page_size`` independently — the
    bar re-renders its label and bounds-checks the current page on
    every setter. :meth:`on_change` registers a callback fired with
    the new page number after each Prev / Next click; the underlying
    Qt buttons do not emit signals directly.
    """

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
        """Set the total item count. Negative values are clamped to 0."""
        self._total = max(0, value)
        self._render()
        return self

    def page(self, value: int) -> Self:
        """Set the current page (1-based). Values below 1 are clamped to 1."""
        self._page = max(1, value)
        self._render()
        return self

    def page_size(self, value: int) -> Self:
        """Set the items-per-page count. Values below 1 are clamped to 1."""
        self._page_size = max(1, value)
        self._render()
        return self

    def on_change(self, callback: Callable[[int], object]) -> Self:
        """Register a callback fired with the new page number on Prev / Next."""
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
