from __future__ import annotations

from collections.abc import Callable
from typing import overload

from PySide6.QtWidgets import QCheckBox, QRadioButton, QWidget
from typing_extensions import Self

from kirei_ui.utils import keep_callback


class KireiCheckbox(QCheckBox):
    """Boolean toggle with a label and the KireiUI fluent API.

    Wraps :class:`QCheckBox`. Setters return ``Self``; the underlying
    ``toggled`` signal is exposed via :meth:`on_change`, which keeps the
    handler alive on the widget so PySide6 will not garbage-collect it.
    """

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kirei", "checkbox")
        self.setProperty("kireiRole", "checkbox")

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        """Get the current label (no arg) or set it (chainable)."""
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def checked(self, value: bool = True) -> Self:
        """Set the checked state. Chainable equivalent of :meth:`setChecked`."""
        self.setChecked(value)
        return self

    def is_checked(self) -> bool:
        """Return the current checked state."""
        return self.isChecked()

    def on_change(self, callback: Callable[[bool], object]) -> Self:
        """Fire on every checked-state change. Receives the new boolean."""
        handler = keep_callback(self, callback)
        self.toggled.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the widget."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self


class KireiRadio(QRadioButton):
    """Mutually exclusive choice button with the KireiUI fluent API.

    Wraps :class:`QRadioButton`. Group membership is implicit via the
    parent widget — Qt only allows one radio in a parent to be checked
    at a time. Same chainable shape as :class:`KireiCheckbox`.
    """

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kirei", "radio")
        self.setProperty("kireiRole", "radio")

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        """Get the current label (no arg) or set it (chainable)."""
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def checked(self, value: bool = True) -> Self:
        """Set the checked state. Selecting one radio unselects siblings."""
        self.setChecked(value)
        return self

    def is_checked(self) -> bool:
        """Return the current checked state."""
        return self.isChecked()

    def on_change(self, callback: Callable[[bool], object]) -> Self:
        """Fire on every checked-state change. Receives the new boolean."""
        handler = keep_callback(self, callback)
        self.toggled.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the widget."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self
