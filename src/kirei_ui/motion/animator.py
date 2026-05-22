from __future__ import annotations

from typing import Any

from PySide6.QtCore import QEasingCurve, QPropertyAnimation
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget

from kirei_ui.utils import attached_list


class KireiAnimator:
    """Static helpers for the animation primitives used across KireiUI.

    All methods animate a Qt property on a widget (or a graphics
    effect) using :class:`QPropertyAnimation` with an out-cubic easing
    curve. Active animations are kept alive on the widget under the
    ``_kirei_animations`` attribute via :func:`attached_list` so
    PySide6 will not garbage-collect them mid-flight.

    When ``enabled=False`` the helpers skip the animation entirely and
    apply the end value synchronously, returning ``None``.
    """

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
        """Animate any Qt property on ``widget`` from ``start_value`` to ``end_value``.

        ``duration`` defaults to 180ms. ``property_name`` may be a
        property exposed by Qt (in which case the matching ``setX``
        method is preferred when animations are disabled) or a custom
        Qt dynamic property.
        """
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
        """Fade ``widget`` in from opacity 0 → 1, calling :meth:`show` first.

        Reuses an existing :class:`QGraphicsOpacityEffect` when one is
        already attached, otherwise installs a new one. When animations
        are disabled, the opacity is set to 1.0 synchronously.
        """
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
        """Fade ``widget`` from opacity 1 → 0.

        Does not call :meth:`hide` — connect to the returned
        animation's ``finished`` signal if you need to hide the widget
        when the fade-out completes.
        """
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
        """Animate ``maximumWidth`` between two values.

        Sets ``minimumWidth`` to the smaller of the two endpoints so
        the widget can actually shrink to the target.
        """
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
        """Animate ``maximumHeight`` between two values.

        Sets ``minimumHeight`` to the smaller of the two endpoints so
        the widget can actually shrink to the target.
        """
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
    attached_list(widget, "_kirei_animations").append(animation)


def _remove_animation(widget: QWidget, animation: QPropertyAnimation) -> None:
    animations = getattr(widget, "_kirei_animations", None)
    if not animations:
        return
    try:
        animations.remove(animation)
    except ValueError:
        return
