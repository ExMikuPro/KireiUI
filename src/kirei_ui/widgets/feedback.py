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

from kirei_ui.locale import KireiTexts
from kirei_ui.motion import KireiAnimator, KireiMotionMixin
from kirei_ui.utils import clear_layout, keep_callback, refresh_style


class KireiAlert(QFrame):
    """Inline alert banner with title, description, variant and a close button.

    Use semantic shortcuts (:meth:`info` / :meth:`success` /
    :meth:`warning` / :meth:`danger`) to flip ``kireiVariant``. The
    close button is hidden by default — call :meth:`closable` to show
    it. :meth:`on_close` registers a callback that runs after the
    alert hides itself.
    """

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
        """Set the alert title (the bold heading line)."""
        self._title.setText(value)
        return self

    def description(self, value: str) -> Self:
        """Set the wrapped description shown under the title."""
        self._description.setText(value)
        return self

    def variant(self, name: str) -> Self:
        """Set the ``kireiVariant`` Qt property and re-polish QSS."""
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def info(self) -> Self:
        """Shortcut for ``variant("info")``."""
        return self.variant("info")

    def success(self) -> Self:
        """Shortcut for ``variant("success")``."""
        return self.variant("success")

    def warning(self) -> Self:
        """Shortcut for ``variant("warning")``."""
        return self.variant("warning")

    def danger(self) -> Self:
        """Shortcut for ``variant("danger")``."""
        return self.variant("danger")

    def closable(self, value: bool = True) -> Self:
        """Show / hide the trailing close button."""
        self._close_button.setVisible(value)
        return self

    def on_close(self, callback: Callable[[], object]) -> Self:
        """Register a callback fired after the close button hides the alert."""
        def handler() -> object:
            self.hide()
            return callback()

        saved = keep_callback(self, handler)
        self._close_button.clicked.connect(saved)
        return self


class KireiBadge(QLabel):
    """Compact status pill rendered as a styled :class:`QLabel`.

    Variants drive ``kireiVariant`` (default / primary / success /
    warning / danger / neutral); QSS handles the colors and rounding.
    """

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
        """Get the current text (no arg) or set it (chainable)."""
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def variant(self, name: str) -> Self:
        """Set the ``kireiVariant`` Qt property and re-polish QSS."""
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def default(self) -> Self:
        """Shortcut for ``variant("default")``."""
        return self.variant("default")

    def primary(self) -> Self:
        """Shortcut for ``variant("primary")``."""
        return self.variant("primary")

    def success(self) -> Self:
        """Shortcut for ``variant("success")``."""
        return self.variant("success")

    def warning(self) -> Self:
        """Shortcut for ``variant("warning")``."""
        return self.variant("warning")

    def danger(self) -> Self:
        """Shortcut for ``variant("danger")``."""
        return self.variant("danger")

    def neutral(self) -> Self:
        """Shortcut for ``variant("neutral")``."""
        return self.variant("neutral")


class KireiTag(QFrame):
    """Removable text chip with optional close button.

    Same variant taxonomy as :class:`KireiBadge`, plus a close button
    that hides the tag (toggled with :meth:`closable`). :meth:`on_close`
    runs after the tag hides itself.
    """

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
        """Set the chip's text."""
        self._label.setText(value)
        return self
    def variant(self, name: str) -> Self:
        """Set the ``kireiVariant`` Qt property and re-polish QSS."""
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def default(self) -> Self:
        """Shortcut for ``variant("default")``."""
        return self.variant("default")

    def primary(self) -> Self:
        """Shortcut for ``variant("primary")``."""
        return self.variant("primary")

    def success(self) -> Self:
        """Shortcut for ``variant("success")``."""
        return self.variant("success")

    def warning(self) -> Self:
        """Shortcut for ``variant("warning")``."""
        return self.variant("warning")

    def danger(self) -> Self:
        """Shortcut for ``variant("danger")``."""
        return self.variant("danger")

    def closable(self, value: bool = True) -> Self:
        """Show / hide the trailing close button."""
        self._close_button.setVisible(value)
        return self

    def on_close(self, callback: Callable[[], object]) -> Self:
        """Register a callback fired after the close button hides the tag."""
        def handler() -> object:
            self.hide()
            return callback()

        saved = keep_callback(self, handler)
        self._close_button.clicked.connect(saved)
        return self


class KireiProgress(QProgressBar, KireiMotionMixin):
    """Progress bar with semantic variants and animated value updates.

    Wraps :class:`QProgressBar`. :meth:`set_value` (and the ``value(int)``
    overload) animate from the current value to the target via
    :meth:`KireiAnimator.animate_property`, unless the bar is hidden,
    in indeterminate mode (``range(0, 0)``), or animations are
    explicitly disabled.

    :meth:`indeterminate` flips between determinate (range 0–100) and
    indeterminate modes; ``kireiState`` mirrors the mode for QSS.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "progress")
        self.setProperty("kireiRole", "progress")
        self.setProperty("kireiVariant", "default")

    def range(self, minimum: int, maximum: int) -> Self:
        """Set the progress range (use ``0, 0`` for indeterminate)."""
        self.setRange(minimum, maximum)
        return self

    @overload
    def value(self) -> int: ...

    @overload
    def value(self, value: int) -> Self: ...

    def value(self, value: int | None = None) -> int | Self:
        """Get the current value (no arg) or animate to ``value`` (chainable)."""
        if value is None:
            return int(super().value())
        return self.set_value(value)

    def set_value(self, value: int, animated: bool | None = None) -> Self:
        """Animate the bar to ``value``.

        Animation is skipped when the bar is in indeterminate mode
        (``min == max == 0``), hidden, or when ``animated=False`` is
        passed. Otherwise the duration is resolved from the mixin
        (instance → app → 180ms default).
        """
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
        """Return the current displayed value."""
        return int(super().value())

    def text_visible(self, value: bool = True) -> Self:
        """Show / hide the percentage label rendered on the bar."""
        self.setTextVisible(value)
        return self

    def indeterminate(self, value: bool = True) -> Self:
        """Toggle indeterminate mode.

        When True, the range becomes ``(0, 0)`` (Qt's looping animation)
        and ``kireiState`` is set to ``"indeterminate"``. When False,
        the range is restored to ``(0, 100)`` and the state to ``"normal"``.
        """
        if value:
            self.setRange(0, 0)
            self.setProperty("kireiState", "indeterminate")
        else:
            self.setRange(0, 100)
            self.setProperty("kireiState", "normal")
        refresh_style(self)
        return self

    def variant(self, name: str) -> Self:
        """Set the ``kireiVariant`` Qt property and re-polish QSS."""
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def success(self) -> Self:
        """Shortcut for ``variant("success")``."""
        return self.variant("success")

    def warning(self) -> Self:
        """Shortcut for ``variant("warning")``."""
        return self.variant("warning")

    def danger(self) -> Self:
        """Shortcut for ``variant("danger")``."""
        return self.variant("danger")


class KireiSpinner(QLabel):
    """Loading spinner rendered as a styled :class:`QLabel`.

    The spin animation itself is driven by QSS targeting the
    ``kireiState`` property (``"running"`` / ``"stopped"``). Default
    text comes from :attr:`KireiTexts.spinner_default`.
    """

    def __init__(self, text: str | None = None, parent: QWidget | None = None) -> None:
        super().__init__(KireiTexts.spinner_default if text is None else text, parent)
        self.setProperty("kirei", "spinner")
        self.setProperty("kireiRole", "spinner")
        self.setProperty("kireiState", "running")
        self.setProperty("kireiSize", "default")

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

    def start(self) -> Self:
        """Show the spinner and set ``kireiState`` to ``"running"``."""
        self.setVisible(True)
        self.setProperty("kireiState", "running")
        refresh_style(self)
        return self

    def stop(self) -> Self:
        """Hide the spinner and set ``kireiState`` to ``"stopped"``."""
        self.setVisible(False)
        self.setProperty("kireiState", "stopped")
        refresh_style(self)
        return self

    def running(self, value: bool = True) -> Self:
        """Boolean form of :meth:`start` / :meth:`stop`."""
        return self.start() if value else self.stop()

    def sized(self, name: str) -> Self:
        """Set the ``kireiSize`` Qt property and re-polish QSS."""
        self.setProperty("kireiSize", name)
        refresh_style(self)
        return self

    @overload
    def size(self) -> QSize: ...

    @overload
    def size(self, name: str) -> Self: ...

    def size(self, name: str | None = None) -> QSize | Self:
        """Get the Qt :class:`QSize` (no arg) or set the size preset (chainable)."""
        if name is None:
            return super().size()
        return self.sized(name)


class KireiEmpty(QWidget):
    """Empty-state placeholder with title, description and optional action.

    Common pattern for "no results" / "nothing here yet" screens. The
    action slot accepts a single widget (typically a button); calling
    :meth:`action` again replaces the previous one rather than stacking.
    """

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
        """Set the empty-state title."""
        self._title.setText(value)
        return self

    def description(self, value: str) -> Self:
        """Set the wrapped description shown under the title."""
        self._description.setText(value)
        return self

    def action(self, widget: QWidget) -> Self:
        """Replace the action region with a single widget (typically a button)."""
        clear_layout(self._action_container)
        self._action_container.addWidget(widget)
        return self

    def variant(self, name: str) -> Self:
        """Set the ``kireiVariant`` Qt property and re-polish QSS."""
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self
