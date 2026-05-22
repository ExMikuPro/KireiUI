from __future__ import annotations

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from kirei_ui import (
    KireiForm,
    KireiGrid,
    KireiHStack,
    KireiPanel,
    KireiScroll,
    KireiSplitter,
    KireiStack,
    KireiTabs,
    KireiVStack,
)


@pytest.fixture(scope="module", autouse=True)
def _app() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_hstack_and_vstack_chainable() -> None:
    a = QLabel("A")
    b = QLabel("B")
    h = KireiHStack()
    v = KireiVStack()

    assert h.add(a).spacing(8).padding(12).margins(1, 2, 3, 4).stretch() is h
    assert v.add(b).spacing(8).padding(12).margins(1, 2, 3, 4).stretch() is v


def test_vstack_can_add_hstack() -> None:
    nested = KireiHStack().add(QLabel("A"))
    root = KireiVStack()
    assert root.add(nested) is root


def test_stack_qt_layout_types() -> None:
    assert isinstance(KireiHStack().qt_layout(), QHBoxLayout)
    assert isinstance(KireiVStack().qt_layout(), QVBoxLayout)


def test_grid_api() -> None:
    grid = KireiGrid()
    assert (
        grid.add_at(QLabel("A"), 0, 0)
        .spacing(8)
        .horizontal_spacing(10)
        .vertical_spacing(12)
        .padding(4)
        .margins(1, 2, 3, 4)
        .clear()
        is grid
    )
    assert isinstance(grid.qt_layout(), QGridLayout)


def test_form_api() -> None:
    form = KireiForm()
    assert (
        form.add_row("Name", QLabel("Alice"))
        .spacing(8)
        .padding(8)
        .margins(1, 2, 3, 4)
        .clear()
        is form
    )
    assert isinstance(form.qt_layout(), QFormLayout)


def test_scroll_api() -> None:
    scroll = KireiScroll()
    content = KireiVStack().add(QLabel("A"))
    assert (
        scroll.content(content)
        .resizable(True)
        .horizontal_policy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        .vertical_policy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        is scroll
    )


def test_panel_api() -> None:
    panel = KireiPanel()
    child = QWidget()
    assert (
        panel.content(child)
        .padding(12)
        .margins(1, 2, 3, 4)
        .variant("card")
        .object_name("main_panel")
        is panel
    )
    assert panel.property("variant") == "card"
    assert panel.objectName() == "main_panel"


def test_splitter_api() -> None:
    splitter = KireiSplitter.horizontal().add(QWidget()).add(QWidget()).sizes([1, 2])
    assert isinstance(splitter, KireiSplitter)
    assert splitter.orientation() == Qt.Orientation.Horizontal

    vertical = KireiSplitter.vertical()
    assert vertical.orientation() == Qt.Orientation.Vertical


def test_stack_api() -> None:
    a = QWidget()
    b = QWidget()
    stack = KireiStack().add_page("a", a).add_page("b", b).current("b")
    assert stack.page("a") is a
    assert stack.page("b") is b
    assert stack.current_index(0) is stack


def test_tabs_api() -> None:
    tabs = KireiTabs().add_tab("One", QWidget()).add_tab("Two", QWidget()).current_index(1)
    assert tabs.tabs_closable(True) is tabs
