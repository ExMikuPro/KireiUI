from __future__ import annotations

from collections.abc import Callable
from typing import Literal, overload

from PySide6.QtCore import QEasingCurve, QEvent, QSize, Qt, QTimer, QVariantAnimation
from PySide6.QtGui import QColor, QCursor, QEnterEvent, QIcon
from PySide6.QtWidgets import QApplication, QPushButton, QToolButton, QWidget
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

# Variants that paint a solid coloured surface — icons must use the
# on-brand text colour to stay legible. All other variants follow the
# theme's default glyph colour.
_SOLID_VARIANTS: frozenset[str] = frozenset({"primary", "danger", "warning", "success"})

# Per-variant token key (in the ``color`` group) that supplies the
# *normal* background. Resolved against the running ``KireiApp``'s
# active token table, so the hover animation always starts from the
# colour QSS is actually painting. ``None`` means the variant has no
# painted normal background (transparent surfaces handled separately).
_VARIANT_NORMAL_TOKEN: dict[str, str | None] = {
    "default": "bg_surface",
    "primary": "primary",
    "danger": "danger",
    "warning": "warning",
    "subtle": None,
    "link": None,
}

# Variants whose hover animation is skipped entirely. ``link`` uses
# QSS-driven text-colour hover only; ``primary`` / ``warning`` /
# ``danger`` paint a QSS gradient as their normal state and
# ``QVariantAnimation`` cannot interpolate gradients — animating them
# would collapse the gradient to a flat colour on hover, so leave
# them to QSS' instant :hover.
_NO_HOVER_VARIANTS: frozenset[str] = frozenset({"link", "primary", "warning", "danger"})

# How strongly the hover state mixes a near-white tint into the
# variant's normal background. Small enough to read as a lift rather
# than a colour change. The tint colour itself is pulled from the
# active theme (``bg_muted``) so dark themes stay dark.
_HOVER_TINT_RATIO = 0.12

# Fallback hex used when the theme's ``bg_muted`` token is missing —
# a neutral gray-white that reads correctly on light themes.
_HOVER_TINT_FALLBACK = "#F4F5F7"

_HOVER_ANIMATION_DURATION_MS = 160

# Debounce window applied to hover enter/leave events. Filters out the
# rapid Enter→Leave→Enter bursts Qt emits when the cursor crosses the
# button's edge, child widget boundaries, or focus rings — those bursts
# would otherwise restart the animation each time and look like a flicker.
_HOVER_DEBOUNCE_MS = 30


def _parse_color(value: str) -> QColor:
    """Parse a colour string from the variant map, accepting ``"transparent"``."""
    if value == "transparent":
        return QColor(0, 0, 0, 0)
    return QColor(value)


def _mix_color(source: QColor, target: QColor, ratio: float) -> QColor:
    """Return ``source`` blended toward ``target`` by ``ratio`` (0..1)."""
    ratio = max(0.0, min(1.0, ratio))

    r = round(source.red() + (target.red() - source.red()) * ratio)
    g = round(source.green() + (target.green() - source.green()) * ratio)
    b = round(source.blue() + (target.blue() - source.blue()) * ratio)

    return QColor(r, g, b, source.alpha())


def _active_color_token(key: str, fallback: str) -> str:
    """Look ``key`` up in the running app's ``color`` token group.

    Returns ``fallback`` whenever no :class:`KireiApp` is running or
    the token is missing — keeps tests that use a plain QApplication
    working without forcing every caller to handle ``None``.
    """
    app = QApplication.instance()
    getter = getattr(app, "active_tokens", None)
    if getter is None:
        return fallback
    tokens = getter()
    return tokens.get("color", {}).get(key, fallback)


def _hover_tint_color() -> QColor:
    """Return the near-white tint mixed into hover backgrounds.

    Reads ``button_hover_tint`` first so themes can pick a hover grey
    that's visibly distinct from their surface colour. Falls back to
    ``bg_muted`` (the pre-existing neutral) and finally to a hardcoded
    light-theme grey, so older theme files without the new token still
    render something sensible.
    """
    explicit = _active_color_token("button_hover_tint", "")
    if explicit:
        return _parse_color(explicit)
    return _parse_color(_active_color_token("bg_muted", _HOVER_TINT_FALLBACK))


def _glyph_color_for_variant(variant: str) -> str | None:
    """Return the icon colour to use for ``variant`` or ``None`` for default."""
    return "#FFFFFF" if variant in _SOLID_VARIANTS else None


def _connect_theme_signal(widget: QWidget, slot: Callable[[], object]) -> None:
    """Wire ``slot`` to the running :class:`KireiApp`'s ``themeChanged``.

    The connection is silently skipped when no QApplication exists or the
    application instance does not expose the signal (e.g. plain
    ``QApplication`` used in tests).
    """
    app = QApplication.instance()
    signal = getattr(app, "themeChanged", None)
    if signal is None:
        return
    signal.connect(slot)
    keep_callback(widget, slot)


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
        animated: bool = True,
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
            animated: When True (default), a 160ms OutCubic background
                colour transition is played on hover-enter / hover-leave.
                Disabled and loading states never animate; setting this
                to False disables hover animation entirely.
            parent: Parent widget.
        """
        super().__init__(text, parent)

        self._variant: ButtonVariant = variant
        self._size: ButtonSize = size
        self._loading = False
        self._normal_text = text
        self._icon_spec: tuple[str, str, int, bool] | None = None
        self._animated = bool(animated)
        self._hover_animation: QVariantAnimation | None = None
        self._hover_active = False

        # Debounce + target-state machine for the hover animation. Without
        # these, Qt's Enter/Leave bursts (cursor crossing the button edge,
        # entering child widgets, focus changes) would each restart the
        # animation from a freshly sampled normal/hover pair and the colour
        # would visibly jump between frames.
        self._hover_debounce_timer = QTimer(self)
        self._hover_debounce_timer.setSingleShot(True)
        self._hover_debounce_timer.setInterval(_HOVER_DEBOUNCE_MS)
        self._hover_debounce_timer.timeout.connect(self._commit_hover_state)
        self._pending_hover_active = False
        self._hover_target: bool | None = None
        self._hover_current_color: QColor | None = None

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("kirei", "button")
        self.setProperty("kireiState", "normal")

        self.set_variant(variant)
        self.set_size(size)
        if icon is not None:
            self.icon(icon, style=icon_style, size=icon_size, strict=strict_icon)

        _connect_theme_signal(self, self._refresh_themed_icon)

    def set_variant(self, variant: ButtonVariant) -> None:
        """Change the variant and re-apply QSS. Non-chainable."""
        previous = getattr(self, "_variant", None)
        self._variant = variant
        self.setProperty("kireiVariant", variant)
        # Drop any inline hover-bg style left over from the previous
        # variant before letting QSS repaint with the new variant's
        # palette. Without this, a primary→subtle switch could keep
        # showing the primary hover blue.
        self._reset_hover_animation_state()
        refresh_style(self)
        # Solid vs flat variants use different glyph colours — repaint the
        # icon when the resolved colour would change.
        if (
            self._icon_spec is not None
            and previous != variant
            and (previous in _SOLID_VARIANTS) != (variant in _SOLID_VARIANTS)
        ):
            self._refresh_themed_icon()

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
            # Loading + disabled must never display a hover background;
            # cancel any in-flight transition and clear the inline style.
            self._reset_hover_animation_state()
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
        argument is a name string. Fluent icons are recoloured on theme
        change; user-supplied :class:`QIcon` instances are used as-is.
        """
        if value is None:
            return super().icon()
        if isinstance(value, QIcon):
            self._icon_spec = None
            self.setIcon(value)
            return self
        self._icon_spec = (value, style, int(size), bool(strict))
        self._refresh_themed_icon()
        return self

    def _refresh_themed_icon(self) -> None:
        if self._icon_spec is None:
            return
        name, style, size, strict = self._icon_spec
        self.setIcon(
            KireiIcon.qicon(
                name,
                style=style,
                size=size,
                color=_glyph_color_for_variant(self._variant),
                strict=strict,
            )
        )

    # ----- Hover background animation -----------------------------------

    def changeEvent(self, event: QEvent) -> None:
        super().changeEvent(event)
        # Disabling the button via setEnabled() bypasses our state
        # accessors, so listen for the underlying Qt notification and
        # tear down any in-flight hover animation. Without this, a
        # button disabled while hovered would keep the inline hover
        # background painted forever.
        if event.type() == QEvent.Type.EnabledChange and not self.isEnabled():
            self._reset_hover_animation_state()
            self._hover_active = False

    def enterEvent(self, event: QEnterEvent) -> None:
        super().enterEvent(event)
        self._hover_active = True
        self._schedule_hover_state(True)

    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self._hover_active = False
        self._schedule_hover_state(False)

    def _should_animate_hover(self) -> bool:
        return (
            self._animated
            and self.isEnabled()
            and not self._loading
            and self._variant_bg_colors() is not None
        )

    def _is_pointer_inside(self) -> bool:
        """Return True when the OS cursor sits inside the button's geometry.

        Used to confirm the hover state at the end of the debounce window
        and at animation completion. Qt's Enter/Leave events lag the real
        cursor when crossing child widgets or focus rings, so polling
        ``QCursor.pos()`` is the only reliable check.
        """
        return self.rect().contains(self.mapFromGlobal(QCursor.pos()))

    def _schedule_hover_state(self, active: bool) -> None:
        """Queue ``active`` as the desired hover state behind a debounce.

        Re-entering during the window cancels the prior pending commit and
        replaces it, so a rapid Enter→Leave→Enter that lands on the same
        final state never starts a new animation. When animations are
        disabled (``animated=False``, loading, disabled) we skip the timer
        entirely and just drop any inline style.
        """
        self._pending_hover_active = active

        if not self._should_animate_hover():
            self._hover_debounce_timer.stop()
            self._reset_hover_animation_state()
            return

        self._hover_debounce_timer.start()

    def _commit_hover_state(self) -> None:
        """Apply the debounced hover state if it still matches reality."""
        if not self._should_animate_hover():
            self._reset_hover_animation_state()
            return

        # Cross-check against the real cursor position. The debounce
        # window may close after a stale Leave event was queued; if the
        # cursor never actually left, suppress the leave animation.
        target = self._pending_hover_active and self._is_pointer_inside()

        if self._hover_target == target and self._hover_animation is not None:
            # Already animating toward the same target — leave it alone.
            return
        if self._hover_target == target and self._hover_current_color is not None:
            # Already settled at the target colour from a previous run.
            return

        self._start_hover_animation(target_hovered=target)

    def _variant_bg_colors(self) -> tuple[QColor, QColor] | None:
        """Return ``(normal, hover)`` QColors for the current variant.

        ``normal`` is read from the running theme's tokens via
        :data:`_VARIANT_NORMAL_TOKEN`, so the animation always starts
        from the colour QSS is actually painting. ``hover`` is that
        colour blended toward the active theme's neutral tint
        (``bg_muted``) by :data:`_HOVER_TINT_RATIO` — a subtle lift
        that reads as a layered grey-white wash on light themes and
        as a soft lighten on dark themes.

        Variants without a normal token (``subtle``) animate from
        transparent toward the tint at full opacity, giving the same
        layered look on flat backgrounds. ``link`` returns ``None``
        to skip the animation entirely.
        """
        if self._variant in _NO_HOVER_VARIANTS:
            return None

        tint = _hover_tint_color()
        token_key = _VARIANT_NORMAL_TOKEN.get(self._variant)

        if token_key is None:
            # Flat / transparent surface (subtle). Hover lays the tint
            # on top at full opacity so the lift is visible against
            # whatever sits behind the button.
            return _parse_color("transparent"), tint

        token_value = _active_color_token(token_key, "")
        if not token_value:
            return None
        normal = _parse_color(token_value)
        # When the normal surface is already at least as light as the
        # tint (e.g. ``default`` sits on ``bg_surface = #FFFFFF`` while
        # the tint is ``bg_muted = #F4F5F7``), mixing 12% of the tint
        # in barely shifts the colour and the animation looks frozen.
        # Snap straight to the tint so the layered grey-white is visible.
        if normal.lightnessF() >= tint.lightnessF():
            return normal, tint
        return normal, _mix_color(normal, tint, _HOVER_TINT_RATIO)

    def _start_hover_animation(self, *, target_hovered: bool) -> None:
        """Run an interpolation toward the requested hover state.

        Animation start uses :attr:`_hover_current_color` when set, so a
        new transition picks up wherever the previous one was interrupted
        instead of snapping back to a fixed normal/hover endpoint. Without
        this, an interrupted leave-animation followed by an enter-animation
        would visibly jump from the partially-faded colour to the variant's
        full normal colour for one frame.
        """
        colors = self._variant_bg_colors()
        if colors is None:
            self._reset_hover_animation_state()
            return

        normal, hover = colors
        end = hover if target_hovered else normal

        if self._hover_current_color is not None:
            start = QColor(self._hover_current_color)
        else:
            start = normal if target_hovered else hover

        self._stop_hover_animation()
        self._hover_target = target_hovered

        if start == end:
            # Already at the right colour — no point in animating, but
            # we still need to make sure the inline style is consistent.
            if not target_hovered:
                self._clear_hover_animation_style()
                self._hover_current_color = None
            else:
                self._apply_hover_background(end)
            return

        animation = QVariantAnimation(self)
        animation.setDuration(_HOVER_ANIMATION_DURATION_MS)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.valueChanged.connect(self._apply_hover_background)

        def _on_finished() -> None:
            # Only release the inline style when the cursor really has
            # left the button. If the user re-entered during the leave
            # animation, the next debounce tick will start an enter
            # animation from the current colour and we must not blank
            # out the background between the two.
            if (
                not target_hovered
                and self._hover_target is False
                and not self._is_pointer_inside()
            ):
                self._clear_hover_animation_style()
                self._hover_current_color = None
            self._hover_animation = None

        animation.finished.connect(_on_finished)
        self._hover_animation = animation
        animation.start()

    def _apply_hover_background(self, value: object) -> None:
        if not isinstance(value, QColor):
            return
        self._hover_current_color = QColor(value)
        if value.alpha() == 0:
            css_color = "transparent"
        elif value.alpha() < 255:
            css_color = value.name(QColor.NameFormat.HexArgb)
        else:
            css_color = value.name(QColor.NameFormat.HexRgb)
        self.setStyleSheet(f'QPushButton[kirei="button"] {{ background: {css_color}; }}')

    def _stop_hover_animation(self) -> None:
        animation = self._hover_animation
        if animation is None:
            return
        animation.stop()
        self._hover_animation = None

    def _clear_hover_animation_style(self) -> None:
        if self.styleSheet():
            self.setStyleSheet("")

    def _reset_hover_animation_state(self) -> None:
        """Tear down all hover animation state.

        Called when the button enters a state in which hover animation
        must not run (loading, disabled, animated=False, variant change,
        unsupported variant). Stops the debounce timer, kills the
        in-flight animation, drops the inline style, and clears the
        cached current colour so the next legitimate hover starts clean.
        """
        self._hover_debounce_timer.stop()
        self._stop_hover_animation()
        self._clear_hover_animation_style()
        self._hover_target = None
        self._hover_current_color = None
        self._pending_hover_active = False


IconButtonShape = Literal["square", "circle"]
IconButtonSize = Literal["compact", "medium", "large"]


_ICON_BUTTON_BOX = {
    "compact": 28,
    "medium": 32,
    "large": 40,
}

_ICON_BUTTON_GLYPH = {
    "compact": 16,
    "medium": 18,
    "large": 22,
}


class KireiIconButton(QToolButton):
    """Square / circular button that shows only an icon.

    Built on :class:`QToolButton` so Qt does not reserve label space.
    Visual variants follow :class:`KireiButton`'s taxonomy
    (``default`` / ``primary`` / ``subtle`` / ``danger`` / ``warning``);
    shape can be ``"square"`` (rounded rect) or ``"circle"``.

    Sizes are presets — ``compact`` (28px box), ``medium`` (32px box,
    the default), ``large`` (40px box). The button is locked to a
    fixed square via ``setFixedSize`` so the icon stays centered
    regardless of the layout.

    QSS hooks: ``kirei="icon-button"``, ``kireiVariant``, ``kireiSize``,
    ``kireiShape``.
    """

    def __init__(
        self,
        icon: str | QIcon | None = None,
        *,
        variant: ButtonVariant = "default",
        size: IconButtonSize = "medium",
        shape: IconButtonShape = "square",
        icon_style: str = "regular",
        strict_icon: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        """Create the icon button.

        Args:
            icon: Fluent icon name (resolved via :class:`KireiIcon`)
                or a pre-built :class:`QIcon`. ``None`` leaves the
                button without an icon (rarely useful).
            variant: Initial visual variant.
            size: Initial size preset.
            shape: ``"square"`` for rounded-rect, ``"circle"`` for
                fully rounded.
            icon_style: ``"regular"`` or ``"filled"``. Only used when
                ``icon`` is a string.
            strict_icon: Raise :class:`KeyError` when the icon name
                cannot be resolved instead of returning a blank icon.
            parent: Parent widget.
        """
        super().__init__(parent)

        self._variant: ButtonVariant = variant
        self._size: IconButtonSize = size
        self._shape: IconButtonShape = shape
        self._icon_spec: tuple[str, str, bool] | None = None

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("kirei", "icon-button")
        self.setProperty("kireiState", "normal")
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setAutoRaise(False)

        self.set_variant(variant)
        self.set_size(size)
        self.set_shape(shape)
        if icon is not None:
            self.icon(icon, style=icon_style, strict=strict_icon)

        _connect_theme_signal(self, self._refresh_themed_icon)

    def set_variant(self, variant: ButtonVariant) -> None:
        """Change the variant and re-apply QSS. Non-chainable."""
        previous = getattr(self, "_variant", None)
        self._variant = variant
        self.setProperty("kireiVariant", variant)
        refresh_style(self)
        if (
            self._icon_spec is not None
            and previous != variant
            and (previous in _SOLID_VARIANTS) != (variant in _SOLID_VARIANTS)
        ):
            self._refresh_themed_icon()

    def set_size(self, size: IconButtonSize) -> None:
        """Change the size preset, resize the button, and re-apply QSS."""
        previous = getattr(self, "_size", None)
        self._size = size
        box = _ICON_BUTTON_BOX[size]
        glyph = _ICON_BUTTON_GLYPH[size]
        self.setFixedSize(box, box)
        self.setIconSize(QSize(glyph, glyph))
        self.setProperty("kireiSize", size)
        refresh_style(self)
        if self._icon_spec is not None and previous != size:
            self._refresh_themed_icon()

    def set_shape(self, shape: IconButtonShape) -> None:
        """Change the shape preset and re-apply QSS."""
        self._shape = shape
        self.setProperty("kireiShape", shape)
        refresh_style(self)

    def variant(self, variant: ButtonVariant) -> Self:
        """Chainable :meth:`set_variant`."""
        self.set_variant(variant)
        return self

    def sized(self, size: IconButtonSize) -> Self:
        """Chainable :meth:`set_size`."""
        self.set_size(size)
        return self

    def shape(self, shape: IconButtonShape) -> Self:
        """Chainable :meth:`set_shape`."""
        self.set_shape(shape)
        return self

    def primary(self) -> Self:
        """Shortcut for ``variant("primary")``."""
        return self.variant("primary")

    def default(self) -> Self:
        """Shortcut for ``variant("default")``."""
        return self.variant("default")

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

    def large(self) -> Self:
        """Shortcut for ``sized("large")``."""
        return self.sized("large")

    def square(self) -> Self:
        """Shortcut for ``shape("square")``."""
        return self.shape("square")

    def circle(self) -> Self:
        """Shortcut for ``shape("circle")``."""
        return self.shape("circle")

    def tooltip(self, value: str) -> Self:
        """Set the hover tooltip text. Recommended on icon-only buttons."""
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
        """Toggle whether the button latches when pressed (toggle button)."""
        self.setCheckable(value)
        return self

    def checked(self, value: bool = True) -> Self:
        """Set the toggled state. Only meaningful with :meth:`checkable` on."""
        self.setChecked(value)
        return self

    def on_click(self, callback: Callable[[], object]) -> Self:
        """Connect a no-arg callback to ``clicked`` (Qt's ``bool`` arg dropped)."""

        def handler(checked: bool = False) -> object:
            _ = checked
            return callback()

        keep_callback(self, handler)
        self.clicked.connect(handler)
        return self

    def on_click_checked(self, callback: Callable[[bool], object]) -> Self:
        """Connect a callback receiving the checkbox-style ``bool`` state."""

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
        strict: bool = False,
    ) -> Self: ...

    def icon(
        self,
        value: str | QIcon | None = None,
        *,
        style: str = "regular",
        strict: bool = False,
    ) -> QIcon | Self:
        """Get or set the displayed icon.

        - ``button.icon()`` -- returns the current :class:`QIcon`.
        - ``button.icon("save")`` -- sets a Fluent icon by name.
        - ``button.icon(my_qicon)`` -- sets a pre-built :class:`QIcon`.

        The pixel size is derived from the current size preset, so
        callers do not pass ``size`` here (use :meth:`set_size` instead).
        """
        if value is None:
            return super().icon()
        if isinstance(value, QIcon):
            self._icon_spec = None
            self.setIcon(value)
            return self
        self._icon_spec = (value, style, bool(strict))
        self._refresh_themed_icon()
        return self

    def _refresh_themed_icon(self) -> None:
        if self._icon_spec is None:
            return
        name, style, strict = self._icon_spec
        glyph = _ICON_BUTTON_GLYPH[self._size]
        self.setIcon(
            KireiIcon.qicon(
                name,
                style=style,
                size=glyph,
                color=_glyph_color_for_variant(self._variant),
                strict=strict,
            )
        )
