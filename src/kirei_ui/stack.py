from __future__ import annotations

from typing import overload

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLayout,
    QScrollArea,
    QSplitter,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from typing_extensions import Self

from kirei_ui.utils import clear_layout


class KireiHStack(QWidget):
    """Horizontal box layout with the KireiUI fluent API.

    A thin wrapper around :class:`QHBoxLayout` set on a plain
    :class:`QWidget`, so a stack can sit anywhere a widget can. Setters
    return ``Self`` for chaining; the underlying Qt layout is exposed
    via :meth:`qt_layout` for cases that need raw access.
    """

    def __init__(self, *widgets: QWidget) -> None:
        super().__init__()
        self.setProperty("kirei", "hstack")
        self._layout = QHBoxLayout(self)
        for widget in widgets:
            self.add(widget)

    def add(self, widget: QWidget, stretch: int = 0) -> Self:
        """Append ``widget`` to the row. ``stretch`` follows :meth:`QBoxLayout.addWidget`."""
        self._layout.addWidget(widget, stretch)
        return self

    def add_layout(self, layout: QLayout, stretch: int = 0) -> Self:
        """Append a nested layout (e.g. a :class:`QGridLayout`) to the row."""
        self._layout.addLayout(layout, stretch)
        return self

    def spacing(self, value: int) -> Self:
        """Set inter-widget spacing in pixels."""
        self._layout.setSpacing(value)
        return self

    def padding(self, value: int) -> Self:
        """Set uniform contents margins in pixels."""
        self._layout.setContentsMargins(value, value, value, value)
        return self

    def margins(self, left: int, top: int, right: int, bottom: int) -> Self:
        """Set per-side contents margins in pixels."""
        self._layout.setContentsMargins(left, top, right, bottom)
        return self

    def stretch(self, value: int = 1) -> Self:
        """Append a stretch with weight ``value`` to push later items right."""
        self._layout.addStretch(value)
        return self

    def clear(self) -> Self:
        """Detach every child widget / sub-layout from the stack."""
        clear_layout(self._layout)
        return self

    def qt_layout(self) -> QHBoxLayout:
        """Return the underlying :class:`QHBoxLayout` for direct Qt API access."""
        return self._layout


class KireiVStack(QWidget):
    """Vertical box layout with the KireiUI fluent API.

    Same shape as :class:`KireiHStack` but stacks children top-to-bottom
    using a :class:`QVBoxLayout`.
    """

    def __init__(self, *widgets: QWidget) -> None:
        super().__init__()
        self.setProperty("kirei", "vstack")
        self._layout = QVBoxLayout(self)
        for widget in widgets:
            self.add(widget)

    def add(self, widget: QWidget, stretch: int = 0) -> Self:
        """Append ``widget`` to the column. ``stretch`` follows :meth:`QBoxLayout.addWidget`."""
        self._layout.addWidget(widget, stretch)
        return self

    def add_layout(self, layout: QLayout, stretch: int = 0) -> Self:
        """Append a nested layout to the column."""
        self._layout.addLayout(layout, stretch)
        return self

    def spacing(self, value: int) -> Self:
        """Set inter-widget spacing in pixels."""
        self._layout.setSpacing(value)
        return self

    def padding(self, value: int) -> Self:
        """Set uniform contents margins in pixels."""
        self._layout.setContentsMargins(value, value, value, value)
        return self

    def margins(self, left: int, top: int, right: int, bottom: int) -> Self:
        """Set per-side contents margins in pixels."""
        self._layout.setContentsMargins(left, top, right, bottom)
        return self

    def stretch(self, value: int = 1) -> Self:
        """Append a stretch with weight ``value`` to push later items down."""
        self._layout.addStretch(value)
        return self

    def clear(self) -> Self:
        """Detach every child widget / sub-layout from the stack."""
        clear_layout(self._layout)
        return self

    def qt_layout(self) -> QVBoxLayout:
        """Return the underlying :class:`QVBoxLayout` for direct Qt API access."""
        return self._layout


class KireiGrid(QWidget):
    """Grid layout with chainable cell placement.

    Cells are placed by explicit ``(row, column)`` coordinates with
    optional row / column spans. Spacing can be set uniformly via
    :meth:`spacing` or per-axis via :meth:`horizontal_spacing` /
    :meth:`vertical_spacing`.
    """

    def __init__(self) -> None:
        super().__init__()
        self._layout = QGridLayout(self)

    def add_at(
        self,
        widget: QWidget,
        row: int,
        column: int,
        row_span: int = 1,
        column_span: int = 1,
    ) -> Self:
        """Place ``widget`` at ``(row, column)`` spanning ``row_span x column_span`` cells."""
        self._layout.addWidget(widget, row, column, row_span, column_span)
        return self

    def spacing(self, value: int) -> Self:
        """Set both horizontal and vertical inter-cell spacing in pixels."""
        self._layout.setSpacing(value)
        return self

    def horizontal_spacing(self, value: int) -> Self:
        """Set only the horizontal inter-cell spacing in pixels."""
        self._layout.setHorizontalSpacing(value)
        return self

    def vertical_spacing(self, value: int) -> Self:
        """Set only the vertical inter-cell spacing in pixels."""
        self._layout.setVerticalSpacing(value)
        return self

    def padding(self, value: int) -> Self:
        """Set uniform contents margins in pixels."""
        self._layout.setContentsMargins(value, value, value, value)
        return self

    def margins(self, left: int, top: int, right: int, bottom: int) -> Self:
        """Set per-side contents margins in pixels."""
        self._layout.setContentsMargins(left, top, right, bottom)
        return self

    def clear(self) -> Self:
        """Detach every cell's widget from the grid."""
        clear_layout(self._layout)
        return self

    def qt_layout(self) -> QGridLayout:
        """Return the underlying :class:`QGridLayout` for direct Qt API access."""
        return self._layout


class KireiForm(QWidget):
    """Two-column form layout (label | field) with the KireiUI fluent API.

    Wraps :class:`QFormLayout`. ``label`` may be a string or a widget;
    pair with :class:`KireiInput`, :class:`KireiCheckbox`, etc. as the
    field column.
    """

    def __init__(self) -> None:
        super().__init__()
        self._layout = QFormLayout(self)

    def add_row(self, label: str | QWidget, field: QWidget) -> Self:
        """Append a labelled row. ``label`` becomes a :class:`QLabel` if it is a string."""
        self._layout.addRow(label, field)
        return self

    def spacing(self, value: int) -> Self:
        """Set inter-row spacing in pixels."""
        self._layout.setSpacing(value)
        return self

    def padding(self, value: int) -> Self:
        """Set uniform contents margins in pixels."""
        self._layout.setContentsMargins(value, value, value, value)
        return self

    def margins(self, left: int, top: int, right: int, bottom: int) -> Self:
        """Set per-side contents margins in pixels."""
        self._layout.setContentsMargins(left, top, right, bottom)
        return self

    def clear(self) -> Self:
        """Detach every row from the form."""
        clear_layout(self._layout)
        return self

    def qt_layout(self) -> QFormLayout:
        """Return the underlying :class:`QFormLayout` for direct Qt API access."""
        return self._layout


class KireiScroll(QScrollArea):
    """Scrollable container with chainable configuration.

    Wraps :class:`QScrollArea`. The scrolled widget is set via
    :meth:`content`; in most cases you also want :meth:`resizable`
    so the inner widget grows with the viewport.
    """

    def content(self, widget: QWidget) -> Self:
        """Set the widget that lives inside the scroll viewport."""
        self.setWidget(widget)
        return self

    def resizable(self, value: bool = True) -> Self:
        """When True, the inner widget resizes to fit the viewport."""
        self.setWidgetResizable(value)
        return self

    def horizontal_policy(self, policy: Qt.ScrollBarPolicy) -> Self:
        """Set the horizontal scroll-bar visibility policy."""
        self.setHorizontalScrollBarPolicy(policy)
        return self

    def vertical_policy(self, policy: Qt.ScrollBarPolicy) -> Self:
        """Set the vertical scroll-bar visibility policy."""
        self.setVerticalScrollBarPolicy(policy)
        return self


class KireiPanel(QFrame):
    """Generic styled container that holds a single content widget.

    Useful for QSS-targeted backgrounds and borders without the
    title / description / footer regions of :class:`KireiCard`.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setProperty("kirei", "panel")
        self._content_layout = QVBoxLayout(self)

    def content(self, widget: QWidget) -> Self:
        """Replace the panel's child with ``widget``."""
        clear_layout(self._content_layout)
        self._content_layout.addWidget(widget)
        return self

    def padding(self, value: int) -> Self:
        """Set uniform contents margins in pixels."""
        self._content_layout.setContentsMargins(value, value, value, value)
        return self

    def margins(self, left: int, top: int, right: int, bottom: int) -> Self:
        """Set per-side contents margins in pixels."""
        self._content_layout.setContentsMargins(left, top, right, bottom)
        return self

    def variant(self, name: str) -> Self:
        """Set the ``kireiVariant`` Qt property (no auto re-polish)."""
        self.setProperty("kireiVariant", name)
        return self

    def object_name(self, name: str) -> Self:
        """Set ``QObject.objectName``, useful for ID-targeted QSS rules."""
        self.setObjectName(name)
        return self


class KireiSplitter(QSplitter):
    """Resizable splitter with chainable orientation, child and size APIs.

    Use the :meth:`horizontal` / :meth:`vertical` factory class methods
    to construct, :meth:`add` to append children, and :meth:`sizes` to
    read or set the per-pane size list (in pixels).
    """

    @classmethod
    def horizontal(cls) -> Self:
        """Construct a splitter with horizontal orientation."""
        return cls(Qt.Orientation.Horizontal)

    @classmethod
    def vertical(cls) -> Self:
        """Construct a splitter with vertical orientation."""
        return cls(Qt.Orientation.Vertical)

    def add(self, widget: QWidget) -> Self:
        """Append ``widget`` as the next pane."""
        self.addWidget(widget)
        return self

    @overload
    def sizes(self) -> list[int]: ...

    @overload
    def sizes(self, values: list[int]) -> Self: ...

    def sizes(self, values: list[int] | None = None) -> list[int] | Self:
        """Get the current pane sizes (no arg) or set them (chainable)."""
        if values is None:
            return list(super().sizes())
        self.setSizes(values)
        return self


class KireiStack(QStackedWidget):
    """Named-page stacked widget with chainable navigation.

    Wraps :class:`QStackedWidget`. Pages are registered by string name;
    :meth:`current` switches by name, :meth:`current_index` switches by
    index. :meth:`page` returns the registered widget for ``name`` or
    ``None`` when missing.
    """

    def __init__(self) -> None:
        super().__init__()
        self._pages: dict[str, QWidget] = {}

    def add_page(self, name: str, widget: QWidget) -> Self:
        """Register ``widget`` under ``name`` and add it to the stack."""
        self._pages[name] = widget
        self.addWidget(widget)
        return self

    def current(self, name: str) -> Self:
        """Switch to the page registered under ``name`` (no-op if missing)."""
        widget = self._pages.get(name)
        if widget is not None:
            self.setCurrentWidget(widget)
        return self

    def current_index(self, index: int) -> Self:
        """Switch to the page at the given zero-based index."""
        self.setCurrentIndex(index)
        return self

    def page(self, name: str) -> QWidget | None:
        """Return the widget registered under ``name``, or ``None`` if missing."""
        return self._pages.get(name)


class KireiTabs(QTabWidget):
    """Tabbed container with the KireiUI fluent API.

    Wraps :class:`QTabWidget`. Use :meth:`add_tab` to append a tab,
    :meth:`current_index` to programmatically switch, and
    :meth:`tabs_closable` to show per-tab close buttons.
    """

    def add_tab(self, title: str, widget: QWidget) -> Self:
        """Append a tab labelled ``title`` showing ``widget``."""
        self.addTab(widget, title)
        return self

    def current_index(self, index: int) -> Self:
        """Switch to the tab at the given zero-based index."""
        self.setCurrentIndex(index)
        return self

    def tabs_closable(self, value: bool = True) -> Self:
        """Show / hide per-tab close buttons."""
        self.setTabsClosable(value)
        return self

