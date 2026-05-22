from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QWidget

from kirei_ui.app.application import KireiApp
from kirei_ui.app.window import KireiWindow
from kirei_ui.widgets.button import KireiButton


def test_window_title_returns_self() -> None:
    with patch("kirei_ui.app.window.QMainWindow.__init__", return_value=None), patch(
        "kirei_ui.app.window.KireiWindow.setWindowTitle"
    ):
        window = KireiWindow()
        assert window.title("Demo") is window


def test_window_size_with_args_returns_self() -> None:
    with patch("kirei_ui.app.window.QMainWindow.__init__", return_value=None), patch(
        "kirei_ui.app.window.KireiWindow.resize"
    ):
        window = KireiWindow()
        assert window.size(900, 600) is window


def test_window_size_no_args_returns_qsize() -> None:
    with patch("kirei_ui.app.window.QMainWindow.__init__", return_value=None), patch(
        "kirei_ui.app.window.QMainWindow.size", return_value=QSize(10, 10)
    ):
        window = KireiWindow()
        assert isinstance(window.size(), QSize)


def test_window_content_returns_self() -> None:
    with patch("kirei_ui.app.window.QMainWindow.__init__", return_value=None), patch(
        "kirei_ui.app.window.KireiWindow.setCentralWidget"
    ):
        window = KireiWindow()
        assert window.content(QWidget()) is window


def test_window_set_content_old_api_still_works() -> None:
    with patch("kirei_ui.app.window.QMainWindow.__init__", return_value=None), patch(
        "kirei_ui.app.window.KireiWindow.setCentralWidget"
    ) as mocked_set:
        window = KireiWindow()
        widget = QWidget()
        window.set_content(widget)

    mocked_set.assert_called_once_with(widget)


def test_button_primary_compact_returns_self() -> None:
    button = KireiButton("A")
    assert button.primary().compact() is button


def test_button_on_click_returns_self() -> None:
    button = KireiButton("A")

    def callback() -> None:
        return None

    assert button.on_click(callback) is button


def test_button_on_click_invoked_once_by_click() -> None:
    QApplication.instance() or QApplication([])
    button = KireiButton("A")
    calls = {"count": 0}

    def callback() -> None:
        calls["count"] += 1

    button.on_click(callback)
    button.click()
    assert calls["count"] == 1


def test_button_on_click_ignores_checked_argument() -> None:
    QApplication.instance() or QApplication([])
    button = KireiButton("A").checkable()
    calls = {"count": 0}

    def callback() -> None:
        calls["count"] += 1

    button.on_click(callback)
    button.click()
    assert calls["count"] == 1


def test_button_checkable_on_click_checked_receives_bool() -> None:
    QApplication.instance() or QApplication([])
    values: list[bool] = []
    button = KireiButton("A").checkable().on_click_checked(lambda checked: values.append(checked))

    button.click()
    button.click()
    assert values == [True, False]


def test_button_chain_with_callback_stays_chainable() -> None:
    button = KireiButton("A")
    chained = button.primary().on_click(lambda: None).compact()
    assert chained is button


def test_qt_native_clicked_connect_still_works() -> None:
    QApplication.instance() or QApplication([])
    button = KireiButton("A")
    calls = {"count": 0}

    def callback() -> None:
        calls["count"] += 1

    button.clicked.connect(callback)
    button.click()
    assert calls["count"] == 1


def test_button_text_getter_and_setter_chain() -> None:
    button = KireiButton("A")
    assert button.text() == "A"
    assert button.text("B") is button
    assert button.text() == "B"


def test_app_load_qss_returns_self() -> None:
    with TemporaryDirectory() as tmp:
        qss_file = Path(tmp) / "app.qss"
        qss_file.write_text("QLabel { color: #123; }", encoding="utf-8")

        with patch("kirei_ui.app.application.QApplication.__init__", return_value=None), patch(
            "kirei_ui.app.application.KireiApp.setApplicationName"
        ), patch("kirei_ui.app.application.KireiApp.setOrganizationName"), patch(
            "kirei_ui.app.application.KireiApp.setStyleSheet"
        ), patch("kirei_ui.app.application.KireiApp.styleSheet", return_value=""):
            app = KireiApp(argv=[], theme=None)
            assert app.load_qss(qss_file) is app


def test_app_set_theme_returns_self() -> None:
    with patch("kirei_ui.app.application.QApplication.__init__", return_value=None), patch(
        "kirei_ui.app.application.KireiApp.setApplicationName"
    ), patch("kirei_ui.app.application.KireiApp.setOrganizationName"), patch(
        "kirei_ui.app.application.KireiApp.setStyleSheet"
    ):
        app = KireiApp(argv=[], theme=None)
        assert app.set_theme(theme="base") is app
        assert app.theme("base") is app
