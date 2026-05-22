from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from PySide6.QtWidgets import QComboBox, QWidget
from typing_extensions import Self

from kirei_ui.utils import keep_callback


class KireiComboBox(QComboBox):
    """Drop-down selector with the KireiUI fluent API.

    Wraps :class:`QComboBox`. Items can carry a hidden ``data`` payload
    (Qt's ``userData``); read it back via :meth:`get_data` after the
    user selects an entry. The ``currentTextChanged`` signal is exposed
    through :meth:`on_change`.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "combobox")
        self.setProperty("kireiRole", "combobox")

    def add_item(self, text: str, data: object | None = None) -> Self:
        """Append a single entry. ``data`` is stored as Qt ``userData``."""
        self.addItem(text, userData=data)
        return self

    def add_items(self, items: Iterable[str]) -> Self:
        """Append multiple text-only entries in one call."""
        self.addItems(list(items))
        return self

    def current(self, value: str) -> Self:
        """Select the first item whose text equals ``value`` (no-op if missing)."""
        index = self.findText(value)
        if index >= 0:
            self.setCurrentIndex(index)
        return self

    def current_index(self, index: int) -> Self:
        """Select an entry by its zero-based index."""
        self.setCurrentIndex(index)
        return self

    def get_value(self) -> str:
        """Return the currently selected item's text."""
        return self.currentText()

    def get_data(self) -> Any:
        """Return the ``userData`` payload of the currently selected item."""
        return self.currentData()

    def on_change(self, callback: Callable[[str], object]) -> Self:
        """Fire when the selected entry changes. Receives the new text."""
        handler = keep_callback(self, callback)
        self.currentTextChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the combo box."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self
