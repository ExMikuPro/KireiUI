from __future__ import annotations

from collections.abc import Callable
from typing import overload

from PySide6.QtGui import QAction, QIcon
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

from kirei_ui.icons import KireiIcon
from kirei_ui.motion import KireiAnimator, KireiMotionMixin
from kirei_ui.utils import keep_callback, refresh_style, replace_layout_content


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
        replace_layout_content(self._content_host, widget)
        return self

    def footer(self, widget: QWidget) -> Self:
        replace_layout_content(self._footer_host, widget)
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
        replace_layout_content(self._content_host, widget)
        return self

    def set_actions(self, widget: QWidget) -> Self:
        replace_layout_content(self._actions_host, widget)
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
        replace_layout_content(self._leading, widget)
        return self

    def trailing(self, widget: QWidget) -> Self:
        replace_layout_content(self._trailing, widget)
        return self

    def content(self, widget: QWidget) -> Self:
        replace_layout_content(self._content, widget)
        return self


class KireiNavItem(QPushButton):
    def __init__(self, text: str = "", key: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kirei", "nav-item")
        self.setProperty("kireiRole", "navItem")
        self.setProperty("kireiState", "normal")
        self._key = key

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        if value is None:
            return super().text()
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
        if value is None:
            return super().icon()
        if isinstance(value, QIcon):
            self.setIcon(value)
            return self
        self.setIcon(KireiIcon.qicon(value, style=style, size=size, strict=strict))
        return self

    def get_key(self) -> str:
        return self._key


class KireiSidebar(QFrame, KireiMotionMixin):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "sidebar")
        self.setProperty("kireiRole", "sidebar")
        self.setProperty("kireiState", "expanded")
        self._items: dict[str, KireiNavItem] = {}
        self._on_change_callbacks: list[Callable[[str], object]] = []
        self._layout = QVBoxLayout(self)
        self._expanded_width = 260
        self._collapsed_width = 72
        self.setMinimumWidth(self._collapsed_width)
        self.setMaximumWidth(self._expanded_width)

    def add_item(
        self,
        text: str,
        key: str | None = None,
        *,
        icon: str | QIcon | None = None,
        icon_style: str = "regular",
        icon_size: int = 20,
        strict_icon: bool = False,
    ) -> Self:
        item_key = key or text
        item = KireiNavItem(text, item_key)
        if icon is not None:
            item.icon(icon, style=icon_style, size=icon_size, strict=strict_icon)

        def on_click() -> object:
            self.current(item_key)
            for callback in self._on_change_callbacks:
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
        self._on_change_callbacks.append(callback)
        return self

    def collapse(self, animated: bool | None = None) -> Self:
        self.setProperty("kireiState", "collapsed")
        refresh_style(self)
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.slide_width(
            self,
            self.width() or self._expanded_width,
            self._collapsed_width,
            duration=duration,
            enabled=enabled,
        )
        return self

    def expand(self, animated: bool | None = None) -> Self:
        self.setProperty("kireiState", "expanded")
        refresh_style(self)
        enabled = self.should_animate(animated)
        duration = self.resolved_animation_duration()
        KireiAnimator.slide_width(
            self,
            self.width() or self._collapsed_width,
            self._expanded_width,
            duration=duration,
            enabled=enabled,
        )
        return self

    def collapsed(self, value: bool = True) -> Self:
        if value:
            return self.collapse()
        return self.expand()

    def toggle(self, animated: bool | None = None) -> Self:
        state = self.property("kireiState")
        if state == "collapsed":
            return self.expand(animated=animated)
        return self.collapse(animated=animated)


class KireiToolbar(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "toolbar")
        self.setProperty("kireiRole", "toolbar")
        self._layout = QHBoxLayout(self)

    def add(self, widget: QWidget) -> Self:
        self._layout.addWidget(widget)
        return self

    def add_action(self, action: QAction) -> Self:
        button = QToolButton(self)
        button.setDefaultAction(action)
        self._layout.addWidget(button)
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
        self._on_click_callbacks: list[Callable[[str], object]] = []
        self._layout = QHBoxLayout(self)

    def add_item(self, text: str, key: str | None = None) -> Self:
        item_key = key or text
        button = QToolButton()
        button.setText(text)
        button.setProperty("kireiRole", "breadcrumbItem")

        def handler() -> object:
            for callback in self._on_click_callbacks:
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
        self._on_click_callbacks.append(callback)
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

    def add_action(
        self,
        text: str,
        callback: Callable[[], object] | None = None,
        *,
        icon: str | QIcon | None = None,
        icon_style: str = "regular",
        icon_size: int = 20,
        strict_icon: bool = False,
    ) -> Self:
        action = self.addAction(text)
        if icon is not None:
            if isinstance(icon, QIcon):
                action.setIcon(icon)
            else:
                action.setIcon(
                    KireiIcon.qicon(
                        icon,
                        style=icon_style,
                        size=icon_size,
                        strict=strict_icon,
                    )
                )
        if callback is not None:
            action.triggered.connect(keep_callback(self, callback))
        return self

    def add_separator(self) -> Self:
        super().addSeparator()
        return self

    def popup_at(self, widget: QWidget) -> Self:
        self.popup(widget.mapToGlobal(widget.rect().bottomLeft()))
        return self
