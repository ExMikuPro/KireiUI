from __future__ import annotations

from typing import Any, TypeVar

from PySide6.QtWidgets import QLayout

T = TypeVar("T")


def refresh_style(widget: Any) -> None:
    """Re-polish ``widget``'s QSS after changing a Qt dynamic property.

    QSS attribute selectors (e.g. ``[kireiVariant="primary"]``) only
    re-evaluate when the style is unpolished and re-polished. Call
    this after :meth:`QWidget.setProperty` to make the change visible.
    """
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()


def keep_callback(widget: Any, handler: T) -> T:
    """Keep ``handler`` alive on ``widget`` and return it unchanged.

    PySide6 will garbage-collect short-lived closures bound to Qt
    signals once the local reference is gone. Storing them on the
    widget itself (under ``_kirei_callbacks``) keeps them alive for
    the widget's lifetime.

    Returns the same handler so call sites can wrap inline:
    ``signal.connect(keep_callback(self, handler))``.
    """
    callbacks = attached_list(widget, "_kirei_callbacks")
    callbacks.append(handler)
    return handler


def attached_list(widget: Any, attr_name: str) -> list[Any]:
    """Return a list attached to widget under attr_name, creating it on first access.

    Use this to keep references to handlers / animations / sub-objects alive on the
    widget without losing them to PySide6's weak ref behavior. Centralizing here
    avoids scattering ``setattr(widget, "_xxx", [])`` patterns across the codebase.
    """
    existing = getattr(widget, attr_name, None)
    if existing is None:
        existing = []
        setattr(widget, attr_name, existing)
    return existing


def clear_layout(layout: QLayout) -> None:
    """Detach every child widget / sub-layout from layout."""
    while layout.count() > 0:
        item = layout.takeAt(0)
        if item is None:
            continue
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            continue
        child_layout = item.layout()
        if child_layout is not None:
            clear_layout(child_layout)


def replace_layout_content(layout: QLayout, widget: Any) -> None:
    """Clear the layout, then add a single widget."""
    clear_layout(layout)
    layout.addWidget(widget)


__all__ = [
    "attached_list",
    "clear_layout",
    "keep_callback",
    "refresh_style",
    "replace_layout_content",
]
