from __future__ import annotations

from collections.abc import Callable
from typing import overload

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

from kirei_ui.locale import KireiTexts
from kirei_ui.motion import KireiAnimator, KireiMotionMixin
from kirei_ui.utils import keep_callback, refresh_style, replace_layout_content


class KireiDialog(QDialog, KireiMotionMixin):
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
        replace_layout_content(self._content_host, widget)
        return self

    def footer(self, widget: QWidget) -> Self:
        replace_layout_content(self._footer_host, widget)
        return self

    def modal(self, value: bool = True) -> Self:
        self.setModal(value)
        return self

    def show_animated(self, animated: bool | None = None) -> Self:
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def close_animated(self, animated: bool | None = None) -> Self:
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        animation = KireiAnimator.fade_out(self, duration=duration, enabled=enabled)
        if animation is None:
            super().close()
            return self

        def finalize() -> None:
            super(KireiDialog, self).close()
            effect = self.graphicsEffect()
            if effect is not None:
                effect.deleteLater()
                self.setGraphicsEffect(None)  # type: ignore[arg-type]

        animation.finished.connect(finalize)
        return self

    def open(self) -> Self:  # type: ignore[override]
        self.show_animated()
        return self

    def close_dialog(self) -> Self:
        return self.close_animated()


class KireiConfirm(QDialog, KireiMotionMixin):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "confirm")
        self.setProperty("kireiRole", "confirm")

        self._title = QLabel("")
        self._title.setProperty("kireiRole", "confirmTitle")
        self._description = QLabel("")
        self._description.setProperty("kireiRole", "confirmDescription")
        self._description.setWordWrap(True)

        self._confirm_btn = QPushButton(KireiTexts.confirm_ok)
        self._cancel_btn = QPushButton(KireiTexts.confirm_cancel)

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

    def open(self) -> Self:  # type: ignore[override]
        enabled = self.should_animate()
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def show_animated(self, animated: bool | None = None) -> Self:
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def close_animated(self, animated: bool | None = None) -> Self:
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        animation = KireiAnimator.fade_out(self, duration=duration, enabled=enabled)
        if animation is None:
            super().close()
            return self
        animation.finished.connect(lambda: super(KireiConfirm, self).close())
        return self


class KireiMessageBox(QMessageBox, KireiMotionMixin):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "message-box")
        self.setProperty("kireiRole", "messageBox")
        self.setProperty("kireiVariant", "info")

    def title(self, value: str) -> Self:
        self.setWindowTitle(value)
        return self

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def info(self) -> Self:
        self.setProperty("kireiVariant", "info")
        self.setIcon(QMessageBox.Icon.Information)
        refresh_style(self)
        return self

    def warning(self) -> Self:  # type: ignore[override]
        self.setProperty("kireiVariant", "warning")
        self.setIcon(QMessageBox.Icon.Warning)
        refresh_style(self)
        return self

    def danger(self) -> Self:
        self.setProperty("kireiVariant", "danger")
        self.setIcon(QMessageBox.Icon.Critical)
        refresh_style(self)
        return self

    def open(self) -> Self:  # type: ignore[override]
        enabled = self.should_animate()
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def show_animated(self, animated: bool | None = None) -> Self:
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def close_animated(self, animated: bool | None = None) -> Self:
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        animation = KireiAnimator.fade_out(self, duration=duration, enabled=enabled)
        if animation is None:
            super().close()
            return self
        animation.finished.connect(lambda: super(KireiMessageBox, self).close())
        return self


class KireiDrawer(QDialog, KireiMotionMixin):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "drawer")
        self.setProperty("kireiRole", "drawer")
        self.setProperty("kireiVariant", "right")

        self._title = QLabel("")
        self._title.setProperty("kireiRole", "drawerTitle")
        self._content_host = QVBoxLayout()
        self._expanded_width = 360

        layout = QVBoxLayout(self)
        layout.addWidget(self._title)
        layout.addLayout(self._content_host)

    def title(self, value: str) -> Self:
        self._title.setText(value)
        return self

    def content(self, widget: QWidget) -> Self:
        replace_layout_content(self._content_host, widget)
        return self

    def side(self, value: str) -> Self:
        self.setProperty("kireiVariant", value)
        refresh_style(self)
        return self

    def open(self, animated: bool | None = None) -> Self:  # type: ignore[override]
        target = max(self._expanded_width, self.sizeHint().width())
        self.setMaximumWidth(0)
        self.show()
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.slide_width(self, 0, target, duration=duration, enabled=enabled)
        return self

    def close(self, animated: bool | None = None) -> Self:  # type: ignore[override]
        start = self.width() or self.maximumWidth() or self._expanded_width
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        animation = KireiAnimator.slide_width(
            self,
            start,
            0,
            duration=duration,
            enabled=enabled,
        )
        if animation is None:
            super().close()
            return self

        def finalize() -> None:
            super(KireiDrawer, self).close()
            self.setMaximumWidth(self._expanded_width)

        animation.finished.connect(finalize)
        return self

    def close_drawer(self) -> Self:
        return self.close()

    def toggle(self, animated: bool | None = None) -> Self:
        if self.isVisible():
            return self.close(animated=animated)
        return self.open(animated=animated)


class KireiPopover(QFrame, KireiMotionMixin):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.WindowType.Popup)
        self.setProperty("kirei", "popover")
        self.setProperty("kireiRole", "popover")
        self._layout = QVBoxLayout(self)

    def content(self, widget: QWidget) -> Self:
        replace_layout_content(self._layout, widget)
        return self

    def popup_at(self, widget: QWidget) -> Self:
        self.move(widget.mapToGlobal(widget.rect().bottomLeft()))
        self.show_animated()
        return self

    def show_animated(self, animated: bool | None = None) -> Self:
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def close_animated(self, animated: bool | None = None) -> Self:
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        animation = KireiAnimator.fade_out(self, duration=duration, enabled=enabled)
        if animation is None:
            self.close()
            return self
        animation.finished.connect(self.close)
        return self


class KireiTooltip:
    """Static helper for attaching tooltips with KireiUI motion semantics.

    Tooltips are not full widgets in KireiUI — Qt's native tooltip surface is used.
    This class is a namespace of static helpers; do not instantiate.
    """

    _motion = KireiMotionMixin()

    @staticmethod
    def apply(widget: QWidget, text: str) -> QWidget:
        widget.setToolTip(text)
        return widget

    @staticmethod
    def show_animated(widget: QWidget, text: str, animated: bool | None = None) -> QWidget:
        widget.setToolTip(text)
        enabled = KireiTooltip._motion.should_animate(animated)
        duration = KireiTooltip._motion.resolved_animation_duration()
        KireiAnimator.fade_in(widget, duration=duration, enabled=enabled)
        return widget

    @staticmethod
    def show(widget: QWidget, text: str) -> QWidget:
        return KireiTooltip.show_animated(widget, text)

    @staticmethod
    def close_animated(widget: QWidget, animated: bool | None = None) -> QWidget:
        enabled = KireiTooltip._motion.should_animate(animated)
        duration = KireiTooltip._motion.resolved_animation_duration()
        animation = KireiAnimator.fade_out(widget, duration=duration, enabled=enabled)
        if animation is None:
            widget.hide()
            return widget
        animation.finished.connect(widget.hide)
        return widget

