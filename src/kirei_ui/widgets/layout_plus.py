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
    """Bordered information block with optional title, description, content and footer.

    A card is the typical wrapper for a self-contained piece of information
    inside a page. It composes four optional regions stacked vertically:

        title          (QLabel, role=cardTitle)
        description    (QLabel, role=cardDescription, word-wrap on)
        content        (one widget — usually a layout container)
        footer         (one widget — typically an action row)

    Each region setter returns ``Self`` so a card can be built fluently:

        >>> KireiCard()
        ...     .title("Quick filters")
        ...     .description("Narrow the dataset")
        ...     .content(KireiForm()...)
        ...     .footer(actions)

    Variants are written to ``kireiVariant``; visuals come from QSS.
    Calling :meth:`content` or :meth:`footer` again replaces the previous
    widget rather than stacking, so updating regions on the fly is safe.
    """

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
        """Set the card title."""
        self._title.setText(value)
        return self

    def description(self, value: str) -> Self:
        """Set the wrap-friendly description displayed under the title."""
        self._description.setText(value)
        return self

    def content(self, widget: QWidget) -> Self:
        """Replace the content region with ``widget``.

        The previous content (if any) is detached from the card; pass a
        single container widget if you need multiple children.
        """
        replace_layout_content(self._content_host, widget)
        return self

    def footer(self, widget: QWidget) -> Self:
        """Replace the footer region with ``widget``.

        Common footers are horizontal action button rows
        (``KireiHStack(...)`` or ``KireiActionGroup(...)``).
        """
        replace_layout_content(self._footer_host, widget)
        return self

    def variant(self, name: str) -> Self:
        """Set ``kireiVariant`` for QSS styling and re-polish."""
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self


class KireiSection(QFrame):
    """Page-level section with title, description, header actions and content.

    Header layout: ``[title + description]  ←stretch→  [actions]``.
    The content area sits below the header and accepts a single
    container widget. :meth:`set_actions` and :meth:`content` replace
    rather than append.
    """

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
        """Set the section title."""
        self._title.setText(value)
        return self

    def description(self, value: str) -> Self:
        """Set the description shown under the title."""
        self._description.setText(value)
        return self

    def content(self, widget: QWidget) -> Self:
        """Replace the section's content area with ``widget``."""
        replace_layout_content(self._content_host, widget)
        return self

    def set_actions(self, widget: QWidget) -> Self:
        """Replace the trailing header action region (typically a button row)."""
        replace_layout_content(self._actions_host, widget)
        return self


class KireiTopBar(QFrame):
    """Top-of-page bar with leading / centered-title / trailing slots.

    Three horizontal regions: leading content (typically nav controls),
    a centered title (or custom content widget), and trailing actions.
    Each region setter replaces the slot's previous occupant.
    """

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
        """Set the centered title text."""
        self._title.setText(value)
        return self

    def leading(self, widget: QWidget) -> Self:
        """Replace the leading (left) slot — typically nav buttons."""
        replace_layout_content(self._leading, widget)
        return self

    def trailing(self, widget: QWidget) -> Self:
        """Replace the trailing (right) slot — typically actions."""
        replace_layout_content(self._trailing, widget)
        return self

    def content(self, widget: QWidget) -> Self:
        """Replace the centered slot. Hides the default title."""
        replace_layout_content(self._content, widget)
        return self


class KireiNavItem(QPushButton):
    """Sidebar / nav-bar item rendered as a styled push button.

    Each item carries a ``key`` used by the parent :class:`KireiSidebar`
    to track selection. ``kireiState`` is flipped between ``"selected"``
    and ``"normal"`` by :meth:`selected` so QSS can style the active row.
    """

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
        """Get the current label (no arg) or set it (chainable)."""
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def key(self, value: str) -> Self:
        """Set the routing key paired with this nav item."""
        self._key = value
        return self

    def selected(self, value: bool = True) -> Self:
        """Flip ``kireiState`` between ``"selected"`` and ``"normal"`` and re-polish."""
        self.setProperty("kireiState", "selected" if value else "normal")
        refresh_style(self)
        return self

    def on_click(self, callback: Callable[[], object]) -> Self:
        """Connect a no-arg callback to ``clicked`` (Qt's ``bool`` arg dropped)."""
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
        """Get or set the leading icon.

        With no argument, returns the current :class:`QIcon`. Pass a
        Fluent icon name (string) or a pre-built :class:`QIcon` to set
        it. ``style`` / ``size`` / ``strict`` only apply to name lookups.
        """
        if value is None:
            return super().icon()
        if isinstance(value, QIcon):
            self.setIcon(value)
            return self
        self.setIcon(KireiIcon.qicon(value, style=style, size=size, strict=strict))
        return self

    def get_key(self) -> str:
        """Return the routing key set at construction or via :meth:`key`."""
        return self._key


class KireiSidebar(QFrame, KireiMotionMixin):
    """Vertical navigation rail with collapse / expand animation.

    Holds an ordered list of :class:`KireiNavItem` entries (added via
    :meth:`add_item`) plus arbitrary widgets (:meth:`add_widget`).
    Each item has a string ``key``; selecting one writes its
    ``kireiState`` to ``"selected"`` and clears the others, then
    notifies every callback registered through :meth:`on_change`.

    Width is constrained between ``_collapsed_width`` (72) and
    ``_expanded_width`` (260). :meth:`collapse` / :meth:`expand` animate
    ``maximumWidth`` between the two and update ``kireiState`` so QSS
    can hide labels in the collapsed rail. :meth:`toggle` flips between
    the two based on the current ``kireiState``; :meth:`collapsed`
    accepts a boolean form of the same.
    """

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
        """Append a navigation entry.

        Args:
            text: Visible label.
            key: Routing key. Defaults to ``text`` when not provided.
            icon: Fluent icon name or :class:`QIcon`. ``None`` for no icon.
            icon_style: ``"regular"`` or ``"filled"`` (only used for name lookups).
            icon_size: Pixel size for name lookups.
            strict_icon: Raise :class:`KeyError` on missing icon names.
        """
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
        """Append a non-navigation widget (separator, profile card, etc.)."""
        self._layout.addWidget(widget)
        return self

    def current(self, key: str) -> Self:
        """Mark the item with ``key`` as selected; clears the others."""
        for item_key, item in self._items.items():
            item.selected(item_key == key)
        return self

    def on_change(self, callback: Callable[[str], object]) -> Self:
        """Register a callback fired with the item key on every selection change."""
        self._on_change_callbacks.append(callback)
        return self

    def collapse(self, animated: bool | None = None) -> Self:
        """Animate the rail to the collapsed width and update ``kireiState``."""
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
        """Animate the rail to the expanded width and update ``kireiState``."""
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
        """Boolean form of :meth:`collapse` / :meth:`expand`."""
        if value:
            return self.collapse()
        return self.expand()

    def toggle(self, animated: bool | None = None) -> Self:
        """Flip between collapsed and expanded based on the current state."""
        state = self.property("kireiState")
        if state == "collapsed":
            return self.expand(animated=animated)
        return self.collapse(animated=animated)


class KireiToolbar(QFrame):
    """Horizontal toolbar with widgets, action buttons, separators and stretch.

    Build it with :meth:`add` (any widget), :meth:`add_action` (a
    :class:`QAction` rendered as a :class:`QToolButton`),
    :meth:`separator` for vertical dividers, and :meth:`stretch` to push
    later items to the right.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "toolbar")
        self.setProperty("kireiRole", "toolbar")
        self._layout = QHBoxLayout(self)

    def add(self, widget: QWidget) -> Self:
        """Append an arbitrary widget to the toolbar."""
        self._layout.addWidget(widget)
        return self

    def add_action(self, action: QAction) -> Self:
        """Append a :class:`QAction` rendered as a :class:`QToolButton`."""
        button = QToolButton(self)
        button.setDefaultAction(action)
        self._layout.addWidget(button)
        return self

    def separator(self) -> Self:
        """Append a vertical divider line."""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setProperty("kireiRole", "toolbarSeparator")
        self._layout.addWidget(line)
        return self

    def stretch(self) -> Self:
        """Append a stretch so subsequent items align to the right."""
        self._layout.addStretch(1)
        return self


class KireiBreadcrumbs(QFrame):
    """Breadcrumb trail of clickable :class:`QToolButton` items.

    Each call to :meth:`add_item` appends a button (and a ``"/"`` label
    separator after the first). Click handlers registered via
    :meth:`on_click` receive the item's key — they are not deduplicated,
    so register once.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "breadcrumbs")
        self.setProperty("kireiRole", "breadcrumbs")
        self._on_click_callbacks: list[Callable[[str], object]] = []
        self._layout = QHBoxLayout(self)

    def add_item(self, text: str, key: str | None = None) -> Self:
        """Append a breadcrumb item. ``key`` defaults to ``text`` when omitted."""
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
        """Register a callback fired with the item key on every breadcrumb click."""
        self._on_click_callbacks.append(callback)
        return self


class KireiActionGroup(QFrame):
    """Horizontal group of action buttons with adjustable spacing.

    A thin wrapper used to align a row of buttons in form / card
    footers without re-creating the QHBox boilerplate every time.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "action-group")
        self.setProperty("kireiRole", "actionGroup")
        self._layout = QHBoxLayout(self)

    def add(self, widget: QWidget) -> Self:
        """Append a widget (typically a :class:`KireiButton`)."""
        self._layout.addWidget(widget)
        return self

    def spacing(self, value: int) -> Self:
        """Set the inter-widget spacing in pixels."""
        self._layout.setSpacing(value)
        return self


class KireiMenu(QMenu):
    """Pop-up menu with chainable item / separator / popup builders.

    Use :meth:`add_action` to attach an item with optional Fluent icon
    and callback, :meth:`add_separator` for divider lines, and
    :meth:`popup_at` to anchor the menu under a trigger widget.
    """

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
        """Append a menu item.

        Args:
            text: Visible label.
            callback: Optional no-arg handler invoked when the item is triggered.
            icon: Fluent icon name or :class:`QIcon`. ``None`` for no icon.
            icon_style: ``"regular"`` or ``"filled"`` (only used for name lookups).
            icon_size: Pixel size for name lookups.
            strict_icon: Raise :class:`KeyError` on missing icon names.
        """
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
        """Append a divider line between menu items."""
        super().addSeparator()
        return self

    def popup_at(self, widget: QWidget) -> Self:
        """Show the menu at ``widget``'s bottom-left corner in global coordinates."""
        self.popup(widget.mapToGlobal(widget.rect().bottomLeft()))
        return self
