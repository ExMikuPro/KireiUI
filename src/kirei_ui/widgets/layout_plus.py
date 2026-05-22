from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
from typing_extensions import Self

from kirei_ui.utils import keep_callback, refresh_style


class KireiCard(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "card")
        self.setProperty("kireiRole", "card")
        self.setProperty("kireiVariant", "default")

        self._title = QLabel("")
        self._title.setProperty("kireiRole", "cardTitle")
        self._description = QLabel("")
        self._description.setProperty("kireiRole", "cardDescription")
        self._description.setWordWrap(True)

        self._content_host = QVBoxLayout()
        self._footer_host = QVBoxLayout()

        layout = QVBoxLayout(self)
        layout.addWidget(self._title)
        layout.addWidget(self._description)
        layout.addLayout(self._content_host)
        layout.addLayout(self._footer_host)

    def title(self, value: str) -> Self:
        self._title.setText(value)
        return self

    def description(self, value: str) -> Self:
        self._description.setText(value)
        return self

    def content(self, widget: QWidget) -> Self:
        _replace_layout_content(self._content_host, widget)
        return self

    def footer(self, widget: QWidget) -> Self:
        _replace_layout_content(self._footer_host, widget)
        return self

    def variant(self, name: str) -> Self:
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self


class KireiSection(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "section")
        self.setProperty("kireiRole", "section")

        self._title = QLabel("")
        self._title.setProperty("kireiRole", "sectionTitle")
        self._description = QLabel("")
        self._description.setProperty("kireiRole", "sectionDescription")
        self._description.setWordWrap(True)
        self._actions_host = QHBoxLayout()
        self._content_host = QVBoxLayout()

        header = QHBoxLayout()
        title_col = QVBoxLayout()
        title_col.addWidget(self._title)
        title_col.addWidget(self._description)
        header.addLayout(title_col)
        header.addStretch(1)
        header.addLayout(self._actions_host)

        layout = QVBoxLayout(self)
        layout.addLayout(header)
        layout.addLayout(self._content_host)

    def title(self, value: str) -> Self:
        self._title.setText(value)
        return self

    def description(self, value: str) -> Self:
        self._description.setText(value)
        return self

    def content(self, widget: QWidget) -> Self:
        _replace_layout_content(self._content_host, widget)
        return self

    def actions(self, widget: QWidget) -> Self:
        _replace_layout_content(self._actions_host, widget)
        return self


class KireiTopBar(QFrame):
    def __init__(self, title: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "topbar")
        self.setProperty("kireiRole", "topbar")

        self._leading = QHBoxLayout()
        self._content = QHBoxLayout()
        self._trailing = QHBoxLayout()
        self._title = QLabel(title)
        self._title.setProperty("kireiRole", "topbarTitle")

        self._content.addWidget(self._title)

        layout = QHBoxLayout(self)
        layout.addLayout(self._leading)
        layout.addLayout(self._content)
        layout.addStretch(1)
        layout.addLayout(self._trailing)

    def title(self, value: str) -> Self:
        self._title.setText(value)
        return self

    def leading(self, widget: QWidget) -> Self:
        _replace_layout_content(self._leading, widget)
        return self

    def trailing(self, widget: QWidget) -> Self:
        _replace_layout_content(self._trailing, widget)
        return self

    def content(self, widget: QWidget) -> Self:
        _replace_layout_content(self._content, widget)
        return self


class KireiNavItem(QPushButton):
    def __init__(self, text: str = "", key: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kirei", "nav-item")
        self.setProperty("kireiRole", "navItem")
        self.setProperty("kireiState", "normal")
        self._key = key

    def text(self, value: str) -> Self:
        self.setText(value)
        return self

    def key(self, value: str) -> Self:
        self._key = value
        return self

    def selected(self, value: bool = True) -> Self:
        self.setProperty("kireiState", "selected" if value else "normal")
        refresh_style(self)
        return self

    def on_click(self, callback: Callable[[], object]) -> Self:
        saved = keep_callback(self, callback)
        self.clicked.connect(saved)
        return self

    def get_key(self) -> str:
        return self._key


class KireiSidebar(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "sidebar")
        self.setProperty("kireiRole", "sidebar")
        self._items: dict[str, KireiNavItem] = {}
        self._layout = QVBoxLayout(self)

    def add_item(self, text: str, key: str | None = None) -> Self:
        item_key = key or text
        item = KireiNavItem(text, item_key)

        def on_click() -> object:
            self.current(item_key)
            for callback in getattr(self, "_kirei_callbacks", []):
                callback(item_key)
            return None

        item.on_click(on_click)
        self._items[item_key] = item
        self._layout.addWidget(item)
        return self

    def add_widget(self, widget: QWidget) -> Self:
        self._layout.addWidget(widget)
        return self

    def current(self, key: str) -> Self:
        for item_key, item in self._items.items():
            item.selected(item_key == key)
        return self

    def on_change(self, callback: Callable[[str], object]) -> Self:
        keep_callback(self, callback)
        return self


class KireiToolbar(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "toolbar")
        self.setProperty("kireiRole", "toolbar")
        self._layout = QHBoxLayout(self)

    def add(self, widget: QWidget) -> Self:
        self._layout.addWidget(widget)
        return self

    def separator(self) -> Self:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setProperty("kireiRole", "toolbarSeparator")
        self._layout.addWidget(line)
        return self

    def stretch(self) -> Self:
        self._layout.addStretch(1)
        return self


class KireiBreadcrumbs(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "breadcrumbs")
        self.setProperty("kireiRole", "breadcrumbs")
        self._layout = QHBoxLayout(self)

    def add_item(self, text: str, key: str | None = None) -> Self:
        item_key = key or text
        button = QToolButton()
        button.setText(text)
        button.setProperty("kireiRole", "breadcrumbItem")

        def handler() -> object:
            for callback in getattr(self, "_kirei_callbacks", []):
                callback(item_key)
            return None

        button.clicked.connect(keep_callback(self, handler))
        if self._layout.count() > 0:
            sep = QLabel("/")
            sep.setProperty("kireiRole", "breadcrumbSeparator")
            self._layout.addWidget(sep)
        self._layout.addWidget(button)
        return self

    def on_click(self, callback: Callable[[str], object]) -> Self:
        keep_callback(self, callback)
        return self


class KireiActionGroup(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "action-group")
        self.setProperty("kireiRole", "actionGroup")
        self._layout = QHBoxLayout(self)

    def add(self, widget: QWidget) -> Self:
        self._layout.addWidget(widget)
        return self

    def spacing(self, value: int) -> Self:
        self._layout.setSpacing(value)
        return self


class KireiMenu(QMenu):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "menu")
        self.setProperty("kireiRole", "menu")

    def add_action(self, text: str, callback: Callable[[], object] | None = None) -> Self:
        action = self.addAction(text)
        if callback is not None:
            action.triggered.connect(keep_callback(self, callback))
        return self

    def add_separator(self) -> Self:
        super().addSeparator()
        return self

    def popup_at(self, widget: QWidget) -> Self:
        self.popup(widget.mapToGlobal(widget.rect().bottomLeft()))
        return self


def _replace_layout_content(layout: QHBoxLayout | QVBoxLayout, widget: QWidget) -> None:
    while layout.count() > 0:
        item = layout.takeAt(0)
        child = item.widget()
        if child is not None:
            child.setParent(None)
    layout.addWidget(widget)
