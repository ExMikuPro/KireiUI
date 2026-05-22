from __future__ import annotations

from collections.abc import Callable
from typing import overload

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QCheckBox, QWidget
from typing_extensions import Self

from kirei_ui.motion import KireiMotionMixin
from kirei_ui.utils import keep_callback, refresh_style


class KireiSwitch(QCheckBox, KireiMotionMixin):
    """Toggle switch styled via QSS, mechanically a :class:`QCheckBox`.

    Reuses Qt's checkbox semantics (toggled signal, checked state) but
    presents as a switch through ``kirei="switch"`` / variant / size
    properties. Animation hooks come from :class:`KireiMotionMixin` —
    actual transitions are driven by QSS, not Python code, so the
    mixin is provided for parity with other animated widgets.
    """

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kirei", "switch")
        self.setProperty("kireiRole", "switch")
        self.setProperty("kireiVariant", "default")
        self.setProperty("kireiSize", "default")

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
        """Set the toggled state. Chainable."""
        self.setChecked(value)
        return self

    def is_checked(self) -> bool:
        """Return the current toggled state."""
        return self.isChecked()

    def on_change(self, callback: Callable[[bool], object]) -> Self:
        """Fire on every state change. Receives the new boolean."""
        handler = keep_callback(self, callback)
        self.toggled.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the switch."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self

    def variant(self, name: str) -> Self:
        """Set the ``kireiVariant`` Qt property and re-polish QSS."""
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def sized(self, name: str) -> Self:
        """Set the ``kireiSize`` Qt property and re-polish QSS."""
        self.setProperty("kireiSize", name)
        refresh_style(self)
        return self

    @overload
    def size(self) -> QSize: ...

    @overload
    def size(self, name: str) -> Self: ...

    def size(self, name: str | None = None) -> QSize | Self:
        """Get the Qt :class:`QSize` (no arg) or set the size preset (chainable)."""
        if name is None:
            return super().size()
        return self.sized(name)
