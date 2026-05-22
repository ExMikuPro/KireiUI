from __future__ import annotations

from collections.abc import Callable
from typing import overload

from PySide6.QtGui import QAction, QColor, QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QColorDialog,
    QFileDialog,
    QMenu,
    QMenuBar,
    QStatusBar,
    QSystemTrayIcon,
    QWidget,
)
from typing_extensions import Self

from kirei_ui.icons import KireiIcon
from kirei_ui.utils import keep_callback


class KireiAction:
    """Fluent wrapper around :class:`QAction` for menus, toolbars and shortcuts.

    Owns a :class:`QAction` instance (accessible via :meth:`qt_action`)
    rather than subclassing it, so the same action can be installed in
    multiple containers (menu, toolbar, status bar) without altering its
    parent. All setters return ``Self`` for chaining.
    """

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        self._action = QAction(text, parent)

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        """Get the action's label (no arg) or set it (chainable)."""
        if value is None:
            return self._action.text()
        self._action.setText(value)
        return self

    def icon(
        self,
        value: str | QIcon,
        *,
        style: str = "regular",
        size: int = 20,
        strict: bool = False,
    ) -> Self:
        """Set the action icon.

        ``value`` may be a Fluent icon name (resolved via
        :class:`KireiIcon`) or a pre-built :class:`QIcon`. ``style``,
        ``size``, ``strict`` are only used when ``value`` is a name.
        """
        if isinstance(value, QIcon):
            self._action.setIcon(value)
            return self
        self._action.setIcon(KireiIcon.qicon(value, style=style, size=size, strict=strict))
        return self

    def shortcut(self, value: str) -> Self:
        """Set a keyboard shortcut from a portable Qt key sequence string."""
        self._action.setShortcut(QKeySequence(value))
        return self

    def tooltip(self, value: str) -> Self:
        """Set the hover tooltip shown on toolbar buttons / menu items."""
        self._action.setToolTip(value)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the action."""
        self._action.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self._action.setDisabled(value)
        return self

    def on_trigger(self, callback: Callable[[], object]) -> Self:
        """Connect a no-arg callback to the action's ``triggered`` signal."""
        self._action.triggered.connect(keep_callback(self, callback))
        return self

    def qt_action(self) -> QAction:
        """Return the underlying :class:`QAction` for direct Qt API access."""
        return self._action


class KireiShortcut:
    """Application-level keyboard shortcut bound to a parent widget.

    Wraps :class:`QShortcut`. Unlike :class:`KireiAction`, a shortcut
    is owned by a single widget and triggers without rendering UI.
    """

    def __init__(self, sequence: str, parent: QWidget) -> None:
        self._shortcut = QShortcut(QKeySequence(sequence), parent)

    def on_trigger(self, callback: Callable[[], object]) -> Self:
        """Connect a no-arg callback to the shortcut's ``activated`` signal."""
        self._shortcut.activated.connect(keep_callback(self, callback))
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the shortcut without removing it."""
        self._shortcut.setEnabled(value)
        return self


class KireiMenuBar(QMenuBar):
    """Application menu bar with title-keyed menu lookup.

    Maintains an internal ``title -> QMenu`` map so :meth:`add_action_to`
    can resolve (and create on demand) the right submenu without
    re-creating it on each call.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "menu-bar")
        self.setProperty("kireiRole", "menuBar")
        self._menus: dict[str, QMenu] = {}

    def add_menu(self, title: str) -> QMenu:
        """Create a top-level menu and remember it under ``title``."""
        menu = self.addMenu(title)
        self._menus[title] = menu
        return menu

    def add_action_to(self, menu_title: str, action: KireiAction | QAction) -> Self:
        """Add ``action`` to the named menu, creating the menu if missing."""
        menu = self._menus.get(menu_title)
        if menu is None:
            menu = self.add_menu(menu_title)
        qaction = action.qt_action() if isinstance(action, KireiAction) else action
        menu.addAction(qaction)
        return self


class KireiStatusBar(QStatusBar):
    """Window status bar with a chainable transient-message API.

    Wraps :class:`QStatusBar`. Use :meth:`message` for transient text,
    :meth:`add` for permanent indicators on the right edge.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "status-bar")
        self.setProperty("kireiRole", "statusBar")

    def message(self, value: str, timeout: int = 0) -> Self:
        """Show ``value`` for ``timeout`` ms (``0`` keeps it until cleared)."""
        self.showMessage(value, timeout)
        return self

    def clear(self) -> Self:
        """Clear the active transient message."""
        self.clearMessage()
        return self

    def add(self, widget: QWidget) -> Self:
        """Pin a permanent widget to the right edge of the bar."""
        self.addPermanentWidget(widget)
        return self


class KireiSystemTray(QSystemTrayIcon):
    """System tray icon with a fluent show / activate API.

    Wraps :class:`QSystemTrayIcon`. The platform must support tray
    icons; Qt will silently no-op on environments that don't.
    """

    def __init__(self, icon: QIcon | None = None, parent: QWidget | None = None) -> None:
        super().__init__(icon or QIcon(), parent)
        self.setProperty("kirei", "system-tray")
        self.setProperty("kireiRole", "systemTray")

    def tooltip(self, value: str) -> Self:
        """Set the hover tooltip shown over the tray icon."""
        self.setToolTip(value)
        return self

    def show_tray(self) -> Self:
        """Show the icon in the system tray."""
        self.show()
        return self

    def hide_tray(self) -> Self:
        """Remove the icon from the system tray."""
        self.hide()
        return self

    def on_activate(self, callback: Callable[[QSystemTrayIcon.ActivationReason], object]) -> Self:
        """Fire when the user clicks / double-clicks the tray icon.

        The callback receives the :class:`QSystemTrayIcon.ActivationReason`
        enum so handlers can distinguish single- vs double-click.
        """
        self.activated.connect(keep_callback(self, callback))
        return self


class KireiFileDialog:
    """Static helpers around :class:`QFileDialog`.

    Each method delegates to the matching Qt static dialog and returns
    its native tuple / string. This is a namespace, not a widget — do
    not instantiate.
    """

    @staticmethod
    def open_file(
        parent: QWidget | None = None,
        caption: str = "Open File",
        directory: str = "",
        filter: str = "All Files (*)",
    ) -> tuple[str, str]:
        """Show a native "open file" dialog. Returns ``(path, selected_filter)``."""
        return QFileDialog.getOpenFileName(parent, caption, directory, filter)

    @staticmethod
    def save_file(
        parent: QWidget | None = None,
        caption: str = "Save File",
        directory: str = "",
        filter: str = "All Files (*)",
    ) -> tuple[str, str]:
        """Show a native "save file" dialog. Returns ``(path, selected_filter)``."""
        return QFileDialog.getSaveFileName(parent, caption, directory, filter)

    @staticmethod
    def open_directory(
        parent: QWidget | None = None,
        caption: str = "Open Directory",
        directory: str = "",
    ) -> str:
        """Show a native directory picker. Returns the selected path or ``""``."""
        return QFileDialog.getExistingDirectory(parent, caption, directory)


class KireiColorDialog:
    """Static helper around :class:`QColorDialog`."""

    @staticmethod
    def get_color(initial: QColor | None = None, parent: QWidget | None = None) -> QColor:
        """Show a native color picker. Returns the chosen :class:`QColor`."""
        return QColorDialog.getColor(initial or QColor(), parent)
