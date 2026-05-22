from __future__ import annotations

from typing import Any

from PySide6.QtCore import QEasingCurve, QPropertyAnimation
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget


class KireiAnimator:
    @staticmethod
    def animate_property(
        widget: QWidget,
        property_name: str,
        start_value: Any,
        end_value: Any,
        duration: int | None = None,
        *,
        enabled: bool = True,
    ) -> QPropertyAnimation | None:
        if not enabled:
            _set_target(widget, property_name, end_value)
            return None

        animation = QPropertyAnimation(widget, property_name.encode("utf-8"))
        animation.setDuration(180 if duration is None else max(0, int(duration)))
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)

        _keep_animation(widget, animation)
        animation.finished.connect(lambda: _remove_animation(widget, animation))
        animation.start()
        return animation

    @staticmethod
    def fade_in(
        widget: QWidget,
        duration: int | None = None,
        *,
        enabled: bool = True,
    ) -> QPropertyAnimation | None:
        effect = widget.graphicsEffect()
        if not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)

        widget.show()

        if not enabled:
            effect.setOpacity(1.0)
            return None

        effect.setOpacity(0.0)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(180 if duration is None else max(0, int(duration)))
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)

        _keep_animation(widget, animation)
        animation.finished.connect(lambda: _remove_animation(widget, animation))
        animation.start()
        return animation

    @staticmethod
    def fade_out(
        widget: QWidget,
        duration: int | None = None,
        *,
        enabled: bool = True,
    ) -> QPropertyAnimation | None:
        effect = widget.graphicsEffect()
        if not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)

        if not enabled:
            effect.setOpacity(0.0)
            return None

        effect.setOpacity(1.0)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(180 if duration is None else max(0, int(duration)))
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)

        _keep_animation(widget, animation)
        animation.finished.connect(lambda: _remove_animation(widget, animation))
        animation.start()
        return animation

    @staticmethod
    def slide_width(
        widget: QWidget,
        start_width: int,
        end_width: int,
        duration: int | None = None,
        *,
        enabled: bool = True,
    ) -> QPropertyAnimation | None:
        widget.setMinimumWidth(min(start_width, end_width))
        return KireiAnimator.animate_property(
            widget,
            "maximumWidth",
            int(start_width),
            int(end_width),
            duration=duration,
            enabled=enabled,
        )

    @staticmethod
    def slide_height(
        widget: QWidget,
        start_height: int,
        end_height: int,
        duration: int | None = None,
        *,
        enabled: bool = True,
    ) -> QPropertyAnimation | None:
        widget.setMinimumHeight(min(start_height, end_height))
        return KireiAnimator.animate_property(
            widget,
            "maximumHeight",
            int(start_height),
            int(end_height),
            duration=duration,
            enabled=enabled,
        )


def _set_target(widget: QWidget, property_name: str, value: Any) -> None:
    setter = f"set{property_name[0].upper()}{property_name[1:]}"
    fn = getattr(widget, setter, None)
    if callable(fn):
        fn(value)
        return
    widget.setProperty(property_name, value)


def _keep_animation(widget: QWidget, animation: QPropertyAnimation) -> None:
    animations = getattr(widget, "_kirei_animations", None)
    if animations is None:
        animations = []
        widget._kirei_animations = animations
    animations.append(animation)


def _remove_animation(widget: QWidget, animation: QPropertyAnimation) -> None:
    animations = getattr(widget, "_kirei_animations", None)
    if not animations:
        return
    try:
        animations.remove(animation)
    except ValueError:
        return
