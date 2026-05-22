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
    """Modal dialog with title / content / footer slots and fade animations.

    Three composable regions are laid out vertically:

        title       (QLabel, role=dialogTitle)
        content     (one widget — typically a form or message)
        footer      (one widget — typically the action row)

    Show the dialog with :meth:`open` (animated fade-in by default) and
    close it with :meth:`close_dialog` / :meth:`close_animated`. The native
    ``exec()`` / ``accept()`` / ``reject()`` flow still works.

    Animation defaults follow the global :class:`KireiApp` settings; per
    dialog you can override with :meth:`animated` / :meth:`animation_duration`,
    or pass ``animated=False`` to a single call.
    """

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
        """Set the dialog title shown at the top."""
        self._title.setText(value)
        return self

    def content(self, widget: QWidget) -> Self:
        """Replace the content region with ``widget``."""
        replace_layout_content(self._content_host, widget)
        return self

    def footer(self, widget: QWidget) -> Self:
        """Replace the footer region with ``widget`` (typically an action row)."""
        replace_layout_content(self._footer_host, widget)
        return self

    def modal(self, value: bool = True) -> Self:
        """Set the modality. Modal dialogs block their parent window."""
        self.setModal(value)
        return self

    def show_animated(self, animated: bool | None = None) -> Self:
        """Show the dialog with a fade-in transition.

        ``animated=None`` (default) defers to per-instance / app settings;
        pass ``True`` / ``False`` to force.
        """
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def close_animated(self, animated: bool | None = None) -> Self:
        """Close the dialog with a fade-out transition, then call ``close``."""
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
        """Chainable replacement for ``QDialog.open()``.

        Returns ``Self`` (instead of Qt's ``None``) so the call can be
        the last step of a builder chain.
        """
        self.show_animated()
        return self

    def close_dialog(self) -> Self:
        """Animated close — alias of :meth:`close_animated` with default args."""
        return self.close_animated()


class KireiConfirm(QDialog, KireiMotionMixin):
    """Two-button confirmation dialog with title / description and fade animations.

    The layout is fixed: a title, a wrap-friendly description, and a
    confirm / cancel button row aligned to the right. Default button
    labels come from :class:`KireiTexts` and can be overridden per
    instance via :meth:`confirm_text` / :meth:`cancel_text`.

    The buttons are wired to ``accept`` / ``reject``, so the standard
    ``exec()`` flow returns :class:`QDialog.DialogCode` as usual. Use
    :meth:`on_confirm` / :meth:`on_cancel` for fire-and-forget callbacks
    that should run alongside the accept / reject signal.

    Animation defaults follow :class:`KireiApp` settings; override per
    instance with :meth:`animated` / :meth:`animation_duration`, or pass
    ``animated=False`` to a single :meth:`show_animated` /
    :meth:`close_animated` call.
    """

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
        """Set the dialog title (the bold heading)."""
        self._title.setText(value)
        return self

    def description(self, value: str) -> Self:
        """Set the wrapped description shown under the title."""
        self._description.setText(value)
        return self

    def confirm_text(self, value: str) -> Self:
        """Override the confirm button label (default: :attr:`KireiTexts.confirm_ok`)."""
        self._confirm_btn.setText(value)
        return self

    def cancel_text(self, value: str) -> Self:
        """Override the cancel button label (default: :attr:`KireiTexts.confirm_cancel`)."""
        self._cancel_btn.setText(value)
        return self

    def on_confirm(self, callback: Callable[[], object]) -> Self:
        """Register a no-arg callback fired alongside ``accept`` when confirmed."""
        self._confirm_btn.clicked.connect(keep_callback(self, callback))
        return self

    def on_cancel(self, callback: Callable[[], object]) -> Self:
        """Register a no-arg callback fired alongside ``reject`` when cancelled."""
        self._cancel_btn.clicked.connect(keep_callback(self, callback))
        return self

    def open(self) -> Self:  # type: ignore[override]
        """Chainable replacement for ``QDialog.open()``. Fades the dialog in."""
        enabled = self.should_animate()
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def show_animated(self, animated: bool | None = None) -> Self:
        """Show the dialog with a fade-in transition."""
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def close_animated(self, animated: bool | None = None) -> Self:
        """Close the dialog with a fade-out transition."""
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        animation = KireiAnimator.fade_out(self, duration=duration, enabled=enabled)
        if animation is None:
            super().close()
            return self
        animation.finished.connect(lambda: super(KireiConfirm, self).close())
        return self


class KireiMessageBox(QMessageBox, KireiMotionMixin):
    """Themable :class:`QMessageBox` with semantic variants and fade animations.

    Three variants set both ``kireiVariant`` (for QSS) and the native
    Qt icon in lockstep:

    - :meth:`info` — ``"info"`` + :attr:`QMessageBox.Icon.Information`
    - :meth:`warning` — ``"warning"`` + :attr:`QMessageBox.Icon.Warning`
    - :meth:`danger` — ``"danger"`` + :attr:`QMessageBox.Icon.Critical`

    Variants default to ``"info"``. Animations follow the same opt-in
    pattern as :class:`KireiDialog`: per-instance state via
    :meth:`animated` / :meth:`animation_duration`, falling back to the
    :class:`KireiApp` defaults.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "message-box")
        self.setProperty("kireiRole", "messageBox")
        self.setProperty("kireiVariant", "info")

    def title(self, value: str) -> Self:
        """Set the title bar text."""
        self.setWindowTitle(value)
        return self

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        """Get the body text (no arg) or set it (chainable)."""
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def info(self) -> Self:
        """Switch to the info variant (blue, :attr:`QMessageBox.Icon.Information`)."""
        self.setProperty("kireiVariant", "info")
        self.setIcon(QMessageBox.Icon.Information)
        refresh_style(self)
        return self

    def warning(self) -> Self:  # type: ignore[override]
        """Switch to the warning variant (yellow, :attr:`QMessageBox.Icon.Warning`)."""
        self.setProperty("kireiVariant", "warning")
        self.setIcon(QMessageBox.Icon.Warning)
        refresh_style(self)
        return self

    def danger(self) -> Self:
        """Switch to the danger variant (red, :attr:`QMessageBox.Icon.Critical`)."""
        self.setProperty("kireiVariant", "danger")
        self.setIcon(QMessageBox.Icon.Critical)
        refresh_style(self)
        return self

    def open(self) -> Self:  # type: ignore[override]
        """Chainable replacement for ``QMessageBox.open()``. Fades the box in."""
        enabled = self.should_animate()
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def show_animated(self, animated: bool | None = None) -> Self:
        """Show the message box with a fade-in transition."""
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def close_animated(self, animated: bool | None = None) -> Self:
        """Close the message box with a fade-out transition."""
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        animation = KireiAnimator.fade_out(self, duration=duration, enabled=enabled)
        if animation is None:
            super().close()
            return self
        animation.finished.connect(lambda: super(KireiMessageBox, self).close())
        return self


class KireiDrawer(QDialog, KireiMotionMixin):
    """Edge-anchored drawer that slides in / out from one side.

    Layout is fixed to a title row plus a single content slot
    (:meth:`content` replaces, not appends). The drawer side is held in
    ``kireiVariant`` (default ``"right"``); change it with :meth:`side`
    and pair with QSS for left / top / bottom anchoring.

    Open and close are width-driven slide animations: the maximum width
    is animated between ``0`` and ``max(_expanded_width, sizeHint())``.
    Both :meth:`open` and :meth:`close` accept ``animated=False`` for
    instant transitions, and :meth:`toggle` flips between them based on
    visibility. The base :meth:`QDialog.close` is intentionally
    overridden — animation cleanup is handled before delegating.
    """

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
        """Set the drawer title shown above the content."""
        self._title.setText(value)
        return self

    def content(self, widget: QWidget) -> Self:
        """Replace the content region with ``widget``."""
        replace_layout_content(self._content_host, widget)
        return self

    def side(self, value: str) -> Self:
        """Set the anchor side via ``kireiVariant`` (``"left"``, ``"right"``, ...)."""
        self.setProperty("kireiVariant", value)
        refresh_style(self)
        return self

    def open(self, animated: bool | None = None) -> Self:  # type: ignore[override]
        """Show the drawer and animate it sliding to the expanded width."""
        target = max(self._expanded_width, self.sizeHint().width())
        self.setMaximumWidth(0)
        self.show()
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.slide_width(self, 0, target, duration=duration, enabled=enabled)
        return self

    def close(self, animated: bool | None = None) -> Self:  # type: ignore[override]
        """Animate the drawer sliding back to width 0, then call ``QDialog.close``."""
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
        """Alias of :meth:`close` for symmetry with ``open`` / ``close_dialog``."""
        return self.close()

    def toggle(self, animated: bool | None = None) -> Self:
        """Open the drawer if hidden, close it if visible."""
        if self.isVisible():
            return self.close(animated=animated)
        return self.open(animated=animated)


class KireiPopover(QFrame, KireiMotionMixin):
    """Lightweight floating panel anchored to another widget.

    Built on a top-level :class:`QFrame` with :attr:`Qt.WindowType.Popup`,
    so the popover closes itself on outside clicks. Hosts a single
    content widget (:meth:`content` replaces the layout's child).

    Use :meth:`popup_at` to position the popover under a trigger
    widget's bottom-left corner and fade it in. Animation defaults
    follow the standard :class:`KireiMotionMixin` resolution (instance
    override → :class:`KireiApp` settings → default).
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.WindowType.Popup)
        self.setProperty("kirei", "popover")
        self.setProperty("kireiRole", "popover")
        self._layout = QVBoxLayout(self)

    def content(self, widget: QWidget) -> Self:
        """Replace the popover's content with ``widget``."""
        replace_layout_content(self._layout, widget)
        return self

    def popup_at(self, widget: QWidget) -> Self:
        """Show the popover at ``widget``'s bottom-left corner with a fade-in."""
        self.move(widget.mapToGlobal(widget.rect().bottomLeft()))
        self.show_animated()
        return self

    def show_animated(self, animated: bool | None = None) -> Self:
        """Show the popover with a fade-in transition."""
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.fade_in(self, duration=duration, enabled=enabled)
        return self

    def close_animated(self, animated: bool | None = None) -> Self:
        """Close the popover with a fade-out transition."""
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
        """Attach ``text`` as a hover tooltip on ``widget``. Returns the widget."""
        widget.setToolTip(text)
        return widget

    @staticmethod
    def show_animated(widget: QWidget, text: str, animated: bool | None = None) -> QWidget:
        """Set the tooltip and fade the widget in. Returns the widget."""
        widget.setToolTip(text)
        enabled = KireiTooltip._motion.should_animate(animated)
        duration = KireiTooltip._motion.resolved_animation_duration()
        KireiAnimator.fade_in(widget, duration=duration, enabled=enabled)
        return widget

    @staticmethod
    def show(widget: QWidget, text: str) -> QWidget:
        """Alias of :meth:`show_animated` with default arguments."""
        return KireiTooltip.show_animated(widget, text)

    @staticmethod
    def close_animated(widget: QWidget, animated: bool | None = None) -> QWidget:
        """Fade ``widget`` out, then hide it. Returns the widget."""
        enabled = KireiTooltip._motion.should_animate(animated)
        duration = KireiTooltip._motion.resolved_animation_duration()
        animation = KireiAnimator.fade_out(widget, duration=duration, enabled=enabled)
        if animation is None:
            widget.hide()
            return widget
        animation.finished.connect(widget.hide)
        return widget

