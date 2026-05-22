from __future__ import annotations

from collections.abc import Callable

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

    def value(self, value: int) -> Self:
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

    def value(self, value: int) -> Self:
        self.setValue(value)
        return self

    def get_value(self) -> int:
        return int(super().value())

    def step(self, value: int) -> Self:
        self.setSingleStep(value)
        return self

    def prefix(self, value: str) -> Self:
        self.setPrefix(value)
        return self

    def suffix(self, value: str) -> Self:
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

    def value(self, value: float) -> Self:
        self.setValue(value)
        return self

    def get_value(self) -> float:
        return float(super().value())

    def step(self, value: float) -> Self:
        self.setSingleStep(value)
        return self

    def decimals(self, value: int) -> Self:
        self.setDecimals(value)
        return self

    def prefix(self, value: str) -> Self:
        self.setPrefix(value)
        return self

    def suffix(self, value: str) -> Self:
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
