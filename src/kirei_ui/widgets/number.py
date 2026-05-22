from __future__ import annotations

from collections.abc import Callable
from typing import overload

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDoubleSpinBox, QSlider, QSpinBox, QWidget
from typing_extensions import Self

from kirei_ui.utils import keep_callback


class KireiSlider(QSlider):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.setProperty("kirei", "slider")
        self.setProperty("kireiRole", "slider")

    def horizontal(self) -> Self:
        self.setOrientation(Qt.Orientation.Horizontal)
        return self

    def vertical(self) -> Self:
        self.setOrientation(Qt.Orientation.Vertical)
        return self

    def range(self, minimum: int, maximum: int) -> Self:
        self.setRange(minimum, maximum)
        return self

    @overload
    def value(self) -> int: ...

    @overload
    def value(self, value: int) -> Self: ...

    def value(self, value: int | None = None) -> int | Self:
        if value is None:
            return int(super().value())
        self.setValue(value)
        return self

    def get_value(self) -> int:
        return int(super().value())

    def step(self, value: int) -> Self:
        self.setSingleStep(value)
        return self

    def page_step(self, value: int) -> Self:
        self.setPageStep(value)
        return self

    def tick_position(self, position: QSlider.TickPosition) -> Self:
        self.setTickPosition(position)
        return self

    def on_change(self, callback: Callable[[int], object]) -> Self:
        handler = keep_callback(self, callback)
        self.valueChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self


class KireiSpinBox(QSpinBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "spinbox")
        self.setProperty("kireiRole", "spinbox")

    def range(self, minimum: int, maximum: int) -> Self:
        self.setRange(minimum, maximum)
        return self

    @overload
    def value(self) -> int: ...

    @overload
    def value(self, value: int) -> Self: ...

    def value(self, value: int | None = None) -> int | Self:
        if value is None:
            return int(super().value())
        self.setValue(value)
        return self

    def get_value(self) -> int:
        return int(super().value())

    def step(self, value: int) -> Self:
        self.setSingleStep(value)
        return self

    @overload
    def prefix(self) -> str: ...

    @overload
    def prefix(self, value: str) -> Self: ...

    def prefix(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().prefix()
        self.setPrefix(value)
        return self

    @overload
    def suffix(self) -> str: ...

    @overload
    def suffix(self, value: str) -> Self: ...

    def suffix(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().suffix()
        self.setSuffix(value)
        return self

    def on_change(self, callback: Callable[[int], object]) -> Self:
        handler = keep_callback(self, callback)
        self.valueChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self


class KireiDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "double-spinbox")
        self.setProperty("kireiRole", "spinbox")

    def range(self, minimum: float, maximum: float) -> Self:
        self.setRange(minimum, maximum)
        return self

    @overload
    def value(self) -> float: ...

    @overload
    def value(self, value: float) -> Self: ...

    def value(self, value: float | None = None) -> float | Self:
        if value is None:
            return float(super().value())
        self.setValue(value)
        return self

    def get_value(self) -> float:
        return float(super().value())

    def step(self, value: float) -> Self:
        self.setSingleStep(value)
        return self

    @overload
    def decimals(self) -> int: ...

    @overload
    def decimals(self, value: int) -> Self: ...

    def decimals(self, value: int | None = None) -> int | Self:
        if value is None:
            return super().decimals()
        self.setDecimals(value)
        return self

    @overload
    def prefix(self) -> str: ...

    @overload
    def prefix(self, value: str) -> Self: ...

    def prefix(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().prefix()
        self.setPrefix(value)
        return self

    @overload
    def suffix(self) -> str: ...

    @overload
    def suffix(self, value: str) -> Self: ...

    def suffix(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().suffix()
        self.setSuffix(value)
        return self

    def on_change(self, callback: Callable[[float], object]) -> Self:
        handler = keep_callback(self, callback)
        self.valueChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self
