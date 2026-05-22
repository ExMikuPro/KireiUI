from __future__ import annotations

from collections.abc import Callable
from typing import overload

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from typing_extensions import Self

from kirei_ui.motion import KireiAnimator, KireiMotionMixin
from kirei_ui.utils import keep_callback, refresh_style


class KireiAlert(QFrame):
    def __init__(
        self,
        title: str = "",
        description: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "alert")
        self.setProperty("kireiRole", "alert")
        self.setProperty("kireiVariant", "info")

        self._title = QLabel(title)
        self._title.setProperty("kireiRole", "alertTitle")
        self._description = QLabel(description)
        self._description.setProperty("kireiRole", "alertDescription")
        self._description.setWordWrap(True)

        self._close_button = QPushButton("x")
        self._close_button.setProperty("kireiRole", "alertClose")
        self._close_button.setVisible(False)
        self._close_button.clicked.connect(self.hide)

        header = QHBoxLayout()
        header.addWidget(self._title)
        header.addStretch(1)
        header.addWidget(self._close_button)

        layout = QVBoxLayout(self)
        layout.addLayout(header)
        layout.addWidget(self._description)

    def title(self, value: str) -> Self:
        self._title.setText(value)
        return self

    def description(self, value: str) -> Self:
        self._description.setText(value)
        return self

    def variant(self, name: str) -> Self:
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def info(self) -> Self:
        return self.variant("info")

    def success(self) -> Self:
        return self.variant("success")

    def warning(self) -> Self:
        return self.variant("warning")

    def danger(self) -> Self:
        return self.variant("danger")

    def closable(self, value: bool = True) -> Self:
        self._close_button.setVisible(value)
        return self

    def on_close(self, callback: Callable[[], object]) -> Self:
        def handler() -> object:
            self.hide()
            return callback()

        saved = keep_callback(self, handler)
        self._close_button.clicked.connect(saved)
        return self


class KireiBadge(QLabel):
    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kirei", "badge")
        self.setProperty("kireiRole", "badge")
        self.setProperty("kireiVariant", "default")

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def variant(self, name: str) -> Self:
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def default(self) -> Self:
        return self.variant("default")

    def primary(self) -> Self:
        return self.variant("primary")

    def success(self) -> Self:
        return self.variant("success")

    def warning(self) -> Self:
        return self.variant("warning")

    def danger(self) -> Self:
        return self.variant("danger")

    def neutral(self) -> Self:
        return self.variant("neutral")


class KireiTag(QFrame):
    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "tag")
        self.setProperty("kireiRole", "tag")
        self.setProperty("kireiVariant", "default")

        self._label = QLabel(text)
        self._label.setProperty("kireiRole", "tagText")
        self._close_button = QPushButton("x")
        self._close_button.setProperty("kireiRole", "tagClose")
        self._close_button.setVisible(False)
        self._close_button.clicked.connect(self.hide)

        layout = QHBoxLayout(self)
        layout.addWidget(self._label)
        layout.addWidget(self._close_button)

    def text(self, value: str) -> Self:
        self._label.setText(value)
        return self
    def variant(self, name: str) -> Self:
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def default(self) -> Self:
        return self.variant("default")

    def primary(self) -> Self:
        return self.variant("primary")

    def success(self) -> Self:
        return self.variant("success")

    def warning(self) -> Self:
        return self.variant("warning")

    def danger(self) -> Self:
        return self.variant("danger")

    def closable(self, value: bool = True) -> Self:
        self._close_button.setVisible(value)
        return self

    def on_close(self, callback: Callable[[], object]) -> Self:
        def handler() -> object:
            self.hide()
            return callback()

        saved = keep_callback(self, handler)
        self._close_button.clicked.connect(saved)
        return self


class KireiProgress(QProgressBar, KireiMotionMixin):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "progress")
        self.setProperty("kireiRole", "progress")
        self.setProperty("kireiVariant", "default")

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
        return self.set_value(value)

    def set_value(self, value: int, animated: bool | None = None) -> Self:
        if self.minimum() == 0 and self.maximum() == 0:
            self.setValue(value)
            return self
        if not self.isVisible():
            self.setValue(value)
            return self
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        current = int(super().value())
        if current < self.minimum():
            current = self.minimum()
        KireiAnimator.animate_property(
            self,
            "value",
            current,
            value,
            duration=duration,
            enabled=enabled,
        )
        return self

    def get_value(self) -> int:
        return int(super().value())

    def text_visible(self, value: bool = True) -> Self:
        self.setTextVisible(value)
        return self

    def indeterminate(self, value: bool = True) -> Self:
        if value:
            self.setRange(0, 0)
            self.setProperty("kireiState", "indeterminate")
        else:
            self.setRange(0, 100)
            self.setProperty("kireiState", "normal")
        refresh_style(self)
        return self

    def variant(self, name: str) -> Self:
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def success(self) -> Self:
        return self.variant("success")

    def warning(self) -> Self:
        return self.variant("warning")

    def danger(self) -> Self:
        return self.variant("danger")


class KireiSpinner(QLabel):
    def __init__(self, text: str = "Loading...", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kirei", "spinner")
        self.setProperty("kireiRole", "spinner")
        self.setProperty("kireiState", "running")
        self.setProperty("kireiSize", "default")

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def start(self) -> Self:
        self.setVisible(True)
        self.setProperty("kireiState", "running")
        refresh_style(self)
        return self

    def stop(self) -> Self:
        self.setVisible(False)
        self.setProperty("kireiState", "stopped")
        refresh_style(self)
        return self

    def running(self, value: bool = True) -> Self:
        return self.start() if value else self.stop()

    def sized(self, name: str) -> Self:
        self.setProperty("kireiSize", name)
        refresh_style(self)
        return self

    @overload
    def size(self) -> QSize: ...

    @overload
    def size(self, name: str) -> Self: ...

    def size(self, name: str | None = None) -> QSize | Self:
        if name is None:
            return super().size()
        return self.sized(name)


class KireiEmpty(QWidget):
    def __init__(
        self,
        title: str = "",
        description: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "empty")
        self.setProperty("kireiRole", "empty")

        self._title = QLabel(title)
        self._title.setProperty("kireiRole", "emptyTitle")
        self._description = QLabel(description)
        self._description.setProperty("kireiRole", "emptyDescription")
        self._description.setWordWrap(True)

        self._action_container = QHBoxLayout()

        layout = QVBoxLayout(self)
        layout.addWidget(self._title)
        layout.addWidget(self._description)
        layout.addLayout(self._action_container)

    def title(self, value: str) -> Self:
        self._title.setText(value)
        return self

    def description(self, value: str) -> Self:
        self._description.setText(value)
        return self

    def action(self, widget: QWidget) -> Self:
        while self._action_container.count() > 0:
            item = self._action_container.takeAt(0)
            child = item.widget()
            if child is not None:
                child.setParent(None)
        self._action_container.addWidget(widget)
        return self

    def variant(self, name: str) -> Self:
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self
