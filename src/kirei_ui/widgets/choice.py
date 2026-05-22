from __future__ import annotations

from collections.abc import Callable
from typing import overload

from PySide6.QtWidgets import QCheckBox, QRadioButton, QWidget
from typing_extensions import Self


class KireiCheckbox(QCheckBox):
    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self._kirei_callbacks: list[Callable[..., object]] = []
        self.setProperty("kirei", "checkbox")
        self.setProperty("kireiRole", "checkbox")

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def checked(self, value: bool = True) -> Self:
        self.setChecked(value)
        return self

    def is_checked(self) -> bool:
        return self.isChecked()

    def on_change(self, callback: Callable[[bool], object]) -> Self:
        handler = self._keep_callback(callback)
        self.toggled.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self

    def _keep_callback(self, handler: Callable[..., object]) -> Callable[..., object]:
        self._kirei_callbacks.append(handler)
        return handler


class KireiRadio(QRadioButton):
    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self._kirei_callbacks: list[Callable[..., object]] = []
        self.setProperty("kirei", "radio")
        self.setProperty("kireiRole", "radio")

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def checked(self, value: bool = True) -> Self:
        self.setChecked(value)
        return self

    def is_checked(self) -> bool:
        return self.isChecked()

    def on_change(self, callback: Callable[[bool], object]) -> Self:
        handler = self._keep_callback(callback)
        self.toggled.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self

    def _keep_callback(self, handler: Callable[..., object]) -> Callable[..., object]:
        self._kirei_callbacks.append(handler)
        return handler
