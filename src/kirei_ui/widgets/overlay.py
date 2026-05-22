from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from typing_extensions import Self

from kirei_ui.utils import keep_callback, refresh_style


class KireiDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "dialog")
        self.setProperty("kireiRole", "dialog")

        self._title = QLabel("")
        self._title.setProperty("kireiRole", "dialogTitle")
        self._content_host = QVBoxLayout()
        self._footer_host = QHBoxLayout()

        layout = QVBoxLayout(self)
        layout.addWidget(self._title)
        layout.addLayout(self._content_host)
        layout.addLayout(self._footer_host)

    def title(self, value: str) -> Self:
        self._title.setText(value)
        return self

    def content(self, widget: QWidget) -> Self:
        _replace_layout_content(self._content_host, widget)
        return self

    def footer(self, widget: QWidget) -> Self:
        _replace_layout_content(self._footer_host, widget)
        return self

    def modal(self, value: bool = True) -> Self:
        self.setModal(value)
        return self

    def open(self) -> Self:
        self.show()
        return self

    def close_dialog(self) -> Self:
        self.close()
        return self


class KireiConfirm(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "confirm")
        self.setProperty("kireiRole", "confirm")

        self._title = QLabel("")
        self._title.setProperty("kireiRole", "confirmTitle")
        self._description = QLabel("")
        self._description.setProperty("kireiRole", "confirmDescription")
        self._description.setWordWrap(True)

        self._confirm_btn = QPushButton("Confirm")
        self._cancel_btn = QPushButton("Cancel")

        self._confirm_btn.clicked.connect(self.accept)
        self._cancel_btn.clicked.connect(self.reject)

        btns = QHBoxLayout()
        btns.addStretch(1)
        btns.addWidget(self._cancel_btn)
        btns.addWidget(self._confirm_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self._title)
        layout.addWidget(self._description)
        layout.addLayout(btns)

    def title(self, value: str) -> Self:
        self._title.setText(value)
        return self

    def description(self, value: str) -> Self:
        self._description.setText(value)
        return self

    def confirm_text(self, value: str) -> Self:
        self._confirm_btn.setText(value)
        return self

    def cancel_text(self, value: str) -> Self:
        self._cancel_btn.setText(value)
        return self

    def on_confirm(self, callback: Callable[[], object]) -> Self:
        self._confirm_btn.clicked.connect(keep_callback(self, callback))
        return self

    def on_cancel(self, callback: Callable[[], object]) -> Self:
        self._cancel_btn.clicked.connect(keep_callback(self, callback))
        return self

    def open(self) -> Self:
        self.show()
        return self


class KireiMessageBox(QMessageBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "message-box")
        self.setProperty("kireiRole", "messageBox")
        self.setProperty("kireiVariant", "info")

    def title(self, value: str) -> Self:
        self.setWindowTitle(value)
        return self

    def text(self, value: str) -> Self:
        self.setText(value)
        return self

    def info(self) -> Self:
        self.setProperty("kireiVariant", "info")
        self.setIcon(QMessageBox.Icon.Information)
        refresh_style(self)
        return self

    def warning(self) -> Self:
        self.setProperty("kireiVariant", "warning")
        self.setIcon(QMessageBox.Icon.Warning)
        refresh_style(self)
        return self

    def danger(self) -> Self:
        self.setProperty("kireiVariant", "danger")
        self.setIcon(QMessageBox.Icon.Critical)
        refresh_style(self)
        return self

    def open(self) -> Self:
        self.show()
        return self


class KireiDrawer(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "drawer")
        self.setProperty("kireiRole", "drawer")
        self.setProperty("kireiVariant", "right")

        self._title = QLabel("")
        self._title.setProperty("kireiRole", "drawerTitle")
        self._content_host = QVBoxLayout()

        layout = QVBoxLayout(self)
        layout.addWidget(self._title)
        layout.addLayout(self._content_host)

    def title(self, value: str) -> Self:
        self._title.setText(value)
        return self

    def content(self, widget: QWidget) -> Self:
        _replace_layout_content(self._content_host, widget)
        return self

    def side(self, value: str) -> Self:
        self.setProperty("kireiVariant", value)
        refresh_style(self)
        return self

    def open(self) -> Self:
        self.show()
        return self

    def close_drawer(self) -> Self:
        self.close()
        return self


class KireiPopover(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.WindowType.Popup)
        self.setProperty("kirei", "popover")
        self.setProperty("kireiRole", "popover")
        self._layout = QVBoxLayout(self)

    def content(self, widget: QWidget) -> Self:
        _replace_layout_content(self._layout, widget)
        return self

    def popup_at(self, widget: QWidget) -> Self:
        self.move(widget.mapToGlobal(widget.rect().bottomLeft()))
        self.show()
        return self


class KireiTooltip:
    @staticmethod
    def apply(widget: QWidget, text: str) -> QWidget:
        widget.setToolTip(text)
        return widget


def _replace_layout_content(layout: QHBoxLayout | QVBoxLayout, widget: QWidget) -> None:
    while layout.count() > 0:
        item = layout.takeAt(0)
        child = item.widget()
        if child is not None:
            child.setParent(None)
    layout.addWidget(widget)
