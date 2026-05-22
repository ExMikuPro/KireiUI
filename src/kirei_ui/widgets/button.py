from __future__ import annotations

from collections.abc import Callable
from typing import Literal, overload

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QWidget
from typing_extensions import Self

from kirei_ui.icons import KireiIcon

ButtonVariant = Literal[
    "default",
    "primary",
    "link",
    "subtle",
    "danger",
    "warning",
]

ButtonSize = Literal[
    "compact",
    "medium",
]


class KireiButton(QPushButton):
    """AUI-inspired button component for KireiUI."""

    def __init__(
        self,
        text: str = "",
        *,
        icon: str | QIcon | None = None,
        variant: ButtonVariant = "default",
        size: ButtonSize = "medium",
        icon_style: str = "regular",
        icon_size: int = 20,
        strict_icon: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(text, parent)

        self._variant: ButtonVariant = variant
        self._size: ButtonSize = size
        self._loading = False
        self._normal_text = text
        self._kirei_callbacks: list[Callable[..., object]] = []

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("kirei", "button")
        self.setProperty("kireiState", "normal")

        self.set_variant(variant)
        self.set_size(size)
        if icon is not None:
            self.icon(icon, style=icon_style, size=icon_size, strict=strict_icon)

    def set_variant(self, variant: ButtonVariant) -> None:
        self._variant = variant
        self.setProperty("kireiVariant", variant)
        # Backward compatibility for older QSS selectors.
        self.setProperty("variant", variant)
        self._refresh_style()

    def set_size(self, size: ButtonSize) -> None:
        self._size = size
        self.setProperty("kireiSize", size)
        # Backward compatibility for older QSS selectors.
        self.setProperty("size", size)

        self._refresh_style()

    def set_loading(self, loading: bool) -> None:
        self._loading = loading
        self.setProperty("kireiState", "loading" if loading else "normal")
        self.setEnabled(not loading)

        if loading:
            self.setText("处理中...")
        else:
            self.setText(self._normal_text)

        self._refresh_style()

    def variant(self, variant: ButtonVariant) -> Self:
        self.set_variant(variant)
        return self

    def sized(self, size: ButtonSize) -> Self:
        self.set_size(size)
        return self

    def loading(self, loading: bool = True) -> Self:
        self.set_loading(loading)
        return self

    def primary(self) -> Self:
        return self.variant("primary")

    def default(self) -> Self:
        return self.variant("default")

    def link(self) -> Self:
        return self.variant("link")

    def subtle(self) -> Self:
        return self.variant("subtle")

    def danger(self) -> Self:
        return self.variant("danger")

    def warning(self) -> Self:
        return self.variant("warning")

    def compact(self) -> Self:
        return self.sized("compact")

    def medium(self) -> Self:
        return self.sized("medium")

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def tooltip(self, value: str) -> Self:
        self.setToolTip(value)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self

    def checkable(self, value: bool = True) -> Self:
        self.setCheckable(value)
        return self

    def checked(self, value: bool = True) -> Self:
        self.setChecked(value)
        return self

    def on_click(self, callback: Callable[[], object]) -> Self:
        def handler(checked: bool = False) -> object:
            _ = checked
            return callback()

        self._kirei_callbacks.append(handler)
        self.clicked.connect(handler)
        return self

    def on_click_checked(self, callback: Callable[[bool], object]) -> Self:
        def handler(checked: bool = False) -> object:
            return callback(bool(checked))

        self._kirei_callbacks.append(handler)
        self.clicked.connect(handler)
        return self

    def icon(
        self,
        value: str | QIcon,
        *,
        style: str = "regular",
        size: int = 20,
        strict: bool = False,
    ) -> Self:
        if isinstance(value, QIcon):
            self.setIcon(value)
            return self
        self.setIcon(KireiIcon.qicon(value, style=style, size=size, strict=strict))
        return self

    def _refresh_style(self) -> None:
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
