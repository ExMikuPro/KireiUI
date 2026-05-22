from __future__ import annotations

from collections.abc import Callable
from typing import overload

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDoubleSpinBox, QSlider, QSpinBox, QWidget
from typing_extensions import Self

from kirei_ui.utils import keep_callback


class KireiSlider(QSlider):
    """Range slider with the KireiUI fluent API.

    Defaults to horizontal orientation. Use :meth:`vertical` /
    :meth:`horizontal` to switch, and :meth:`tick_position` to draw
    notches under the track.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.setProperty("kirei", "slider")
        self.setProperty("kireiRole", "slider")

    def horizontal(self) -> Self:
        """Switch to horizontal orientation (the default)."""
        self.setOrientation(Qt.Orientation.Horizontal)
        return self

    def vertical(self) -> Self:
        """Switch to vertical orientation."""
        self.setOrientation(Qt.Orientation.Vertical)
        return self

    def range(self, minimum: int, maximum: int) -> Self:
        """Set the inclusive value range."""
        self.setRange(minimum, maximum)
        return self

    @overload
    def value(self) -> int: ...

    @overload
    def value(self, value: int) -> Self: ...

    def value(self, value: int | None = None) -> int | Self:
        """Get the current value (no arg) or set it (chainable)."""
        if value is None:
            return int(super().value())
        self.setValue(value)
        return self

    def get_value(self) -> int:
        """Return the current integer value."""
        return int(super().value())

    def step(self, value: int) -> Self:
        """Set the single-step delta used by arrow keys."""
        self.setSingleStep(value)
        return self

    def page_step(self, value: int) -> Self:
        """Set the page-step delta used by Page Up / Page Down."""
        self.setPageStep(value)
        return self

    def tick_position(self, position: QSlider.TickPosition) -> Self:
        """Configure where tick marks appear relative to the track."""
        self.setTickPosition(position)
        return self

    def on_change(self, callback: Callable[[int], object]) -> Self:
        """Fire on every value change. Receives the new integer."""
        handler = keep_callback(self, callback)
        self.valueChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the slider."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self


class KireiSpinBox(QSpinBox):
    """Integer spin box with the KireiUI fluent API.

    Wraps :class:`QSpinBox`. Use :meth:`prefix` / :meth:`suffix` to
    bracket the displayed value (e.g. ``"$"`` / ``" px"``).
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "spinbox")
        self.setProperty("kireiRole", "spinbox")

    def range(self, minimum: int, maximum: int) -> Self:
        """Set the inclusive integer range."""
        self.setRange(minimum, maximum)
        return self

    @overload
    def value(self) -> int: ...

    @overload
    def value(self, value: int) -> Self: ...

    def value(self, value: int | None = None) -> int | Self:
        """Get the current value (no arg) or set it (chainable)."""
        if value is None:
            return int(super().value())
        self.setValue(value)
        return self

    def get_value(self) -> int:
        """Return the current integer value."""
        return int(super().value())

    def step(self, value: int) -> Self:
        """Set the increment used by the up / down arrows."""
        self.setSingleStep(value)
        return self

    @overload
    def prefix(self) -> str: ...

    @overload
    def prefix(self, value: str) -> Self: ...

    def prefix(self, value: str | None = None) -> str | Self:
        """Get or set the static text rendered before the value."""
        if value is None:
            return super().prefix()
        self.setPrefix(value)
        return self

    @overload
    def suffix(self) -> str: ...

    @overload
    def suffix(self, value: str) -> Self: ...

    def suffix(self, value: str | None = None) -> str | Self:
        """Get or set the static text rendered after the value."""
        if value is None:
            return super().suffix()
        self.setSuffix(value)
        return self

    def on_change(self, callback: Callable[[int], object]) -> Self:
        """Fire on every value change. Receives the new integer."""
        handler = keep_callback(self, callback)
        self.valueChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the spin box."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self


class KireiDoubleSpinBox(QDoubleSpinBox):
    """Floating-point spin box with the KireiUI fluent API.

    Wraps :class:`QDoubleSpinBox`. Same chainable shape as
    :class:`KireiSpinBox`, with :meth:`decimals` controlling the
    displayed precision.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "double-spinbox")
        self.setProperty("kireiRole", "spinbox")

    def range(self, minimum: float, maximum: float) -> Self:
        """Set the inclusive float range."""
        self.setRange(minimum, maximum)
        return self

    @overload
    def value(self) -> float: ...

    @overload
    def value(self, value: float) -> Self: ...

    def value(self, value: float | None = None) -> float | Self:
        """Get the current value (no arg) or set it (chainable)."""
        if value is None:
            return float(super().value())
        self.setValue(value)
        return self

    def get_value(self) -> float:
        """Return the current float value."""
        return float(super().value())

    def step(self, value: float) -> Self:
        """Set the increment used by the up / down arrows."""
        self.setSingleStep(value)
        return self

    @overload
    def decimals(self) -> int: ...

    @overload
    def decimals(self, value: int) -> Self: ...

    def decimals(self, value: int | None = None) -> int | Self:
        """Get or set the number of decimal digits displayed."""
        if value is None:
            return super().decimals()
        self.setDecimals(value)
        return self

    @overload
    def prefix(self) -> str: ...

    @overload
    def prefix(self, value: str) -> Self: ...

    def prefix(self, value: str | None = None) -> str | Self:
        """Get or set the static text rendered before the value."""
        if value is None:
            return super().prefix()
        self.setPrefix(value)
        return self

    @overload
    def suffix(self) -> str: ...

    @overload
    def suffix(self, value: str) -> Self: ...

    def suffix(self, value: str | None = None) -> str | Self:
        """Get or set the static text rendered after the value."""
        if value is None:
            return super().suffix()
        self.setSuffix(value)
        return self

    def on_change(self, callback: Callable[[float], object]) -> Self:
        """Fire on every value change. Receives the new float."""
        handler = keep_callback(self, callback)
        self.valueChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the spin box."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self
