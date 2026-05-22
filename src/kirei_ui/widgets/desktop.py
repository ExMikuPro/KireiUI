from __future__ import annotations

from collections.abc import Callable

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
    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        self._action = QAction(text, parent)

    def text(self, value: str) -> Self:
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
        if isinstance(value, QIcon):
            self._action.setIcon(value)
            return self
        self._action.setIcon(KireiIcon.qicon(value, style=style, size=size, strict=strict))
        return self

    def shortcut(self, value: str) -> Self:
        self._action.setShortcut(QKeySequence(value))
        return self

    def tooltip(self, value: str) -> Self:
        self._action.setToolTip(value)
        return self

    def enabled(self, value: bool = True) -> Self:
        self._action.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self._action.setDisabled(value)
        return self

    def on_trigger(self, callback: Callable[[], object]) -> Self:
        self._action.triggered.connect(keep_callback(self, callback))
        return self

    def qt_action(self) -> QAction:
        return self._action


class KireiShortcut:
    def __init__(self, sequence: str, parent: QWidget) -> None:
        self._shortcut = QShortcut(QKeySequence(sequence), parent)

    def on_trigger(self, callback: Callable[[], object]) -> Self:
        self._shortcut.activated.connect(keep_callback(self, callback))
        return self

    def enabled(self, value: bool = True) -> Self:
        self._shortcut.setEnabled(value)
        return self


class KireiMenuBar(QMenuBar):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "menu-bar")
        self.setProperty("kireiRole", "menuBar")
        self._menus: dict[str, QMenu] = {}

    def add_menu(self, title: str) -> QMenu:
        menu = self.addMenu(title)
        self._menus[title] = menu
        return menu

    def add_action_to(self, menu_title: str, action: KireiAction | QAction) -> Self:
        menu = self._menus.get(menu_title)
        if menu is None:
            menu = self.add_menu(menu_title)
        qaction = action.qt_action() if isinstance(action, KireiAction) else action
        menu.addAction(qaction)
        return self


class KireiStatusBar(QStatusBar):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "status-bar")
        self.setProperty("kireiRole", "statusBar")

    def message(self, value: str, timeout: int = 0) -> Self:
        self.showMessage(value, timeout)
        return self

    def clear(self) -> Self:
        self.clearMessage()
        return self

    def add(self, widget: QWidget) -> Self:
        self.addPermanentWidget(widget)
        return self


class KireiSystemTray(QSystemTrayIcon):
    def __init__(self, icon: QIcon | None = None, parent: QWidget | None = None) -> None:
        super().__init__(icon or QIcon(), parent)
        self.setProperty("kirei", "system-tray")
        self.setProperty("kireiRole", "systemTray")

    def tooltip(self, value: str) -> Self:
        self.setToolTip(value)
        return self

    def show_tray(self) -> Self:
        self.show()
        return self

    def hide_tray(self) -> Self:
        self.hide()
        return self

    def on_activate(self, callback: Callable[[QSystemTrayIcon.ActivationReason], object]) -> Self:
        self.activated.connect(keep_callback(self, callback))
        return self


class KireiFileDialog:
    @staticmethod
    def open_file(
        parent: QWidget | None = None,
        caption: str = "Open File",
        directory: str = "",
        filter: str = "All Files (*)",
    ) -> tuple[str, str]:
        return QFileDialog.getOpenFileName(parent, caption, directory, filter)

    @staticmethod
    def save_file(
        parent: QWidget | None = None,
        caption: str = "Save File",
        directory: str = "",
        filter: str = "All Files (*)",
    ) -> tuple[str, str]:
        return QFileDialog.getSaveFileName(parent, caption, directory, filter)

    @staticmethod
    def open_directory(
        parent: QWidget | None = None,
        caption: str = "Open Directory",
        directory: str = "",
    ) -> str:
        return QFileDialog.getExistingDirectory(parent, caption, directory)


class KireiColorDialog:
    @staticmethod
    def get_color(initial: QColor | None = None, parent: QWidget | None = None) -> QColor:
        return QColorDialog.getColor(initial or QColor(), parent)
