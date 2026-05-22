from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QLineEdit, QTextEdit, QWidget
from typing_extensions import Self


class KireiInput(QLineEdit):
    def __init__(self, value: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._kirei_callbacks: list[Callable[..., object]] = []
        self.setProperty("kirei", "input")
        self.setProperty("kireiRole", "input")
        if value:
            self.setText(value)

    def placeholder(self, value: str) -> Self:
        self.setPlaceholderText(value)
        return self

    def value(self, value: str) -> Self:
        self.setText(value)
        return self

    def get_value(self) -> str:
        return self.text()

    def clearable(self) -> Self:
        self.setClearButtonEnabled(True)
        return self

    def readonly(self, value: bool = True) -> Self:
        self.setReadOnly(value)
        return self

    def max_length(self, value: int) -> Self:
        self.setMaxLength(value)
        return self

    def on_change(self, callback: Callable[[str], object]) -> Self:
        handler = self._keep_callback(callback)
        self.textChanged.connect(handler)
        return self

    def on_submit(self, callback: Callable[[], object]) -> Self:
        def handler() -> object:
            return callback()

        saved = self._keep_callback(handler)
        self.returnPressed.connect(saved)
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


class KireiPassword(KireiInput):
    def __init__(self, value: str = "", parent: QWidget | None = None) -> None:
        super().__init__(value=value, parent=parent)
        self.setProperty("kireiRole", "password")
        self.setEchoMode(QLineEdit.EchoMode.Password)

    def show_password(self, value: bool = True) -> Self:
        mode = QLineEdit.EchoMode.Normal if value else QLineEdit.EchoMode.Password
        self.setEchoMode(mode)
        return self


class KireiTextarea(QTextEdit):
    def __init__(self, value: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._kirei_callbacks: list[Callable[..., object]] = []
        self.setProperty("kirei", "textarea")
        self.setProperty("kireiRole", "textarea")
        if value:
            self.setPlainText(value)

    def placeholder(self, value: str) -> Self:
        self.setPlaceholderText(value)
        return self

    def value(self, value: str) -> Self:
        self.setPlainText(value)
        return self

    def get_value(self) -> str:
        return self.toPlainText()

    def readonly(self, value: bool = True) -> Self:
        self.setReadOnly(value)
        return self

    def on_change(self, callback: Callable[[], object]) -> Self:
        handler = self._keep_callback(callback)
        self.textChanged.connect(handler)
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
