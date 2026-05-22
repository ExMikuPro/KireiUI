from __future__ import annotations

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from kirei_ui import KireiHStack, KireiVStack


@pytest.fixture(scope="module", autouse=True)
def _app() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_hstack_add_returns_self() -> None:
    stack = KireiHStack()
    assert stack.add(QLabel("A")) is stack


def test_vstack_add_returns_self() -> None:
    stack = KireiVStack()
    assert stack.add(QLabel("A")) is stack


def test_spacing_padding_margins_stretch_return_self() -> None:
    hstack = KireiHStack()
    assert hstack.spacing(8) is hstack
    assert hstack.padding(12) is hstack
    assert hstack.margins(1, 2, 3, 4) is hstack
    assert hstack.stretch() is hstack


def test_vstack_can_add_hstack() -> None:
    vstack = KireiVStack()
    nested = KireiHStack().add(QLabel("A"))
    assert vstack.add(nested) is vstack


def test_qt_layout_returns_matching_layout_type() -> None:
    assert isinstance(KireiHStack().qt_layout(), QHBoxLayout)
    assert isinstance(KireiVStack().qt_layout(), QVBoxLayout)


def test_add_layout_returns_self() -> None:
    vstack = KireiVStack()
    raw_layout = QHBoxLayout()
    assert vstack.add_layout(raw_layout) is vstack


def test_clear_returns_self_and_removes_items() -> None:
    stack = KireiHStack().add(QLabel("A")).add(QWidget()).stretch()
    assert stack.qt_layout().count() > 0
    assert stack.clear() is stack
    assert stack.qt_layout().count() == 0
