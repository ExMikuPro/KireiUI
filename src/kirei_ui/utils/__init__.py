from __future__ import annotations

from typing import Any, TypeVar

T = TypeVar("T")


def refresh_style(widget: Any) -> None:
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()


def keep_callback(widget: Any, handler: T) -> T:
    callbacks = getattr(widget, "_kirei_callbacks", None)
    if callbacks is None:
        callbacks = []
        widget._kirei_callbacks = callbacks
    callbacks.append(handler)
    return handler


__all__ = ["keep_callback", "refresh_style"]
