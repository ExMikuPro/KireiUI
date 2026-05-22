from __future__ import annotations

from collections.abc import Callable
from typing import Literal, overload

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QWidget
from typing_extensions import Self

from kirei_ui.icons import KireiIcon
from kirei_ui.locale import KireiTexts
from kirei_ui.utils import keep_callback, refresh_style

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
    """A QPushButton with KireiUI's fluent API and semantic variants.

    KireiButton supports six visual variants — ``default``, ``primary``,
    ``link``, ``subtle``, ``danger``, ``warning`` — and two sizes (``compact``,
    ``medium``). Variants and sizes are exposed both as constructor arguments
    and as chainable shortcut methods, so the following are equivalent:

        >>> KireiButton("Save", variant="primary", size="compact")
        >>> KireiButton("Save").primary().compact()

    Variants and sizes write the corresponding ``kireiVariant`` /
    ``kireiSize`` Qt dynamic property; visual styling lives in QSS, not in
    Python. State changes (``set_loading``) flip ``kireiState`` between
    ``"loading"`` and ``"normal"``.

    The native ``clicked`` signal still works. ``on_click`` and
    ``on_click_checked`` are convenience adapters that drop / forward Qt's
    ``checked`` argument so user callbacks can stay one of:

        >>> button.on_click(lambda: do_save())
        >>> button.on_click_checked(lambda is_checked: ...)

    Loading text comes from ``KireiTexts.button_loading`` so it can be
    localized globally.
    """

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
        """Create a button.

        Args:
            text: Initial button label.
            icon: Either a Fluent icon name (resolved via :class:`KireiIcon`)
                or a :class:`QIcon` instance. ``None`` leaves the button
                without an icon.
            variant: Initial visual variant.
            size: Initial size preset.
            icon_style: ``"regular"`` or ``"filled"``. Only used when
                ``icon`` is a string.
            icon_size: Pixel size of the icon. Only used when ``icon`` is a
                string.
            strict_icon: If True, raise :class:`KeyError` when the icon name
                cannot be resolved instead of returning a blank icon.
            parent: Parent widget.
        """
        super().__init__(text, parent)

        self._variant: ButtonVariant = variant
        self._size: ButtonSize = size
        self._loading = False
        self._normal_text = text

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("kirei", "button")
        self.setProperty("kireiState", "normal")

        self.set_variant(variant)
        self.set_size(size)
        if icon is not None:
            self.icon(icon, style=icon_style, size=icon_size, strict=strict_icon)

    def set_variant(self, variant: ButtonVariant) -> None:
        """Change the variant and re-apply QSS. Non-chainable."""
        self._variant = variant
        self.setProperty("kireiVariant", variant)
        refresh_style(self)

    def set_size(self, size: ButtonSize) -> None:
        """Change the size preset and re-apply QSS. Non-chainable."""
        self._size = size
        self.setProperty("kireiSize", size)
        refresh_style(self)

    def set_loading(self, loading: bool) -> None:
        """Toggle the loading state.

        While loading, the button is disabled, ``kireiState`` becomes
        ``"loading"``, and the label is replaced with
        :attr:`KireiTexts.button_loading`. Restoring also restores the
        original label captured at construction time.
        """
        self._loading = loading
        self.setProperty("kireiState", "loading" if loading else "normal")
        self.setEnabled(not loading)

        if loading:
            self.setText(KireiTexts.button_loading)
        else:
            self.setText(self._normal_text)

        refresh_style(self)

    def variant(self, variant: ButtonVariant) -> Self:
        """Chainable :meth:`set_variant`."""
        self.set_variant(variant)
        return self

    def sized(self, size: ButtonSize) -> Self:
        """Chainable :meth:`set_size`."""
        self.set_size(size)
        return self

    def loading(self, loading: bool = True) -> Self:
        """Chainable :meth:`set_loading`."""
        self.set_loading(loading)
        return self

    def primary(self) -> Self:
        """Shortcut for ``variant("primary")``."""
        return self.variant("primary")

    def default(self) -> Self:
        """Shortcut for ``variant("default")``."""
        return self.variant("default")

    def link(self) -> Self:
        """Shortcut for ``variant("link")``."""
        return self.variant("link")

    def subtle(self) -> Self:
        """Shortcut for ``variant("subtle")``."""
        return self.variant("subtle")

    def danger(self) -> Self:
        """Shortcut for ``variant("danger")``."""
        return self.variant("danger")

    def warning(self) -> Self:
        """Shortcut for ``variant("warning")``."""
        return self.variant("warning")

    def compact(self) -> Self:
        """Shortcut for ``sized("compact")``."""
        return self.sized("compact")

    def medium(self) -> Self:
        """Shortcut for ``sized("medium")``."""
        return self.sized("medium")

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        """Get the current label (no arg) or set it (chainable)."""
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def tooltip(self, value: str) -> Self:
        """Set the hover tooltip text."""
        self.setToolTip(value)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the button."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self

    def checkable(self, value: bool = True) -> Self:
        """Toggle whether the button can be pressed-and-held (toggle button)."""
        self.setCheckable(value)
        return self

    def checked(self, value: bool = True) -> Self:
        """Set the toggled state. Only meaningful with :meth:`checkable` on."""
        self.setChecked(value)
        return self

    def on_click(self, callback: Callable[[], object]) -> Self:
        """Connect a no-arg callback to ``clicked``.

        Qt's ``clicked`` signal emits a ``bool`` for checkable buttons; this
        adapter drops it so plain ``def handler(): ...`` works for both
        checkable and non-checkable buttons.

        For the checked-state value, use :meth:`on_click_checked` instead.
        """
        def handler(checked: bool = False) -> object:
            _ = checked
            return callback()

        keep_callback(self, handler)
        self.clicked.connect(handler)
        return self

    def on_click_checked(self, callback: Callable[[bool], object]) -> Self:
        """Connect a callback receiving the checkbox-style ``bool`` state.

        Useful for ``button.checkable()`` toggles where the consumer needs
        to know the new pressed state.
        """
        def handler(checked: bool = False) -> object:
            return callback(bool(checked))

        keep_callback(self, handler)
        self.clicked.connect(handler)
        return self

    @overload
    def icon(self) -> QIcon: ...

    @overload
    def icon(
        self,
        value: str | QIcon,
        *,
        style: str = "regular",
        size: int = 20,
        strict: bool = False,
    ) -> Self: ...

    def icon(
        self,
        value: str | QIcon | None = None,
        *,
        style: str = "regular",
        size: int = 20,
        strict: bool = False,
    ) -> QIcon | Self:
        """Get or set the button icon.

        - ``button.icon()`` — returns the current :class:`QIcon`.
        - ``button.icon("save")`` — sets a Fluent icon by name.
        - ``button.icon(my_qicon)`` — sets a pre-built :class:`QIcon`.

        ``style``, ``size`` and ``strict`` are only consulted when the first
        argument is a name string.
        """
        if value is None:
            return super().icon()
        if isinstance(value, QIcon):
            self.setIcon(value)
            return self
        self.setIcon(KireiIcon.qicon(value, style=style, size=size, strict=strict))
        return self
