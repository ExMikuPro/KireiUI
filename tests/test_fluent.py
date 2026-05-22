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
from kirei_ui.widgets.choice import KireiCheckbox, KireiRadio
from kirei_ui.widgets.divider import KireiDivider
from kirei_ui.widgets.input import KireiInput, KireiPassword, KireiTextarea
from kirei_ui.widgets.label import KireiLabel, KireiText, KireiTitle
from kirei_ui.widgets.select import KireiComboBox


@pytest.fixture(scope="module", autouse=True)
def _app() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_window_title_returns_self() -> None:
    window = KireiWindow()
    assert window.title("Demo") is window


def test_window_size_with_args_returns_self() -> None:
    window = KireiWindow()
    assert window.size(900, 600) is window


def test_window_size_no_args_returns_qsize() -> None:
    window = KireiWindow()
    assert isinstance(window.size(), QSize)


def test_window_content_returns_self() -> None:
    window = KireiWindow()
    assert window.content(QWidget()) is window


def test_window_set_content_old_api_still_works() -> None:
    window = KireiWindow()
    widget = QWidget()
    window.set_content(widget)
    assert window.centralWidget() is widget


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

        class _FakeApp:
            def __init__(self) -> None:
                self._style = ""

            def styleSheet(self) -> str:
                return self._style

            def setStyleSheet(self, value: str) -> None:
                self._style = value

        app = _FakeApp()
        assert KireiApp.load_qss(app, qss_file) is app


def test_app_set_theme_returns_self() -> None:
    class _FakeApp:
        def __init__(self) -> None:
            self._style = ""

        def setStyleSheet(self, value: str) -> None:
            self._style = value

        def set_theme(
            self,
            theme: str | None = "base",
            qss_files: list[str | Path] | None = None,
            extra_qss: str | None = None,
        ) -> "_FakeApp":
            return KireiApp.set_theme(self, theme=theme, qss_files=qss_files, extra_qss=extra_qss)

    app = _FakeApp()
    assert KireiApp.set_theme(app, theme="base") is app
    assert KireiApp.theme(app, "base") is app


def test_label_text_returns_self() -> None:
    label = KireiLabel()
    assert label.text("A") is label


def test_input_placeholder_returns_self() -> None:
    control = KireiInput()
    assert control.placeholder("A") is control


def test_title_and_text_role_defaults() -> None:
    assert KireiTitle("A").property("kireiRole") == "title"
    assert KireiText("A").property("kireiRole") == "text"


def test_input_value_and_get_value() -> None:
    control = KireiInput()
    assert control.value("A").get_value() == "A"


def test_password_default_echo_mode_is_password() -> None:
    control = KireiPassword()
    assert control.echoMode() == control.EchoMode.Password


def test_checkbox_checked_and_is_checked() -> None:
    control = KireiCheckbox()
    assert control.checked().is_checked() is True


def test_radio_checked_and_is_checked() -> None:
    control = KireiRadio("A")
    assert control.checked().is_checked() is True


def test_textarea_value_and_get_value() -> None:
    control = KireiTextarea()
    assert control.value("A").get_value() == "A"


def test_combobox_add_items_current_and_get_value() -> None:
    control = KireiComboBox()
    assert control.add_items(["A", "B"]).current("B").get_value() == "B"


def test_input_on_change_returns_self() -> None:
    control = KireiInput()
    assert control.on_change(lambda _value: None) is control


def test_input_on_submit_returns_self() -> None:
    control = KireiInput()
    assert control.on_submit(lambda: None) is control


def test_divider_default_role() -> None:
    divider = KireiDivider()
    assert divider.property("kireiRole") == "divider"


def test_button_on_click_returns_self_again() -> None:
    button = KireiButton("A")
    assert button.on_click(lambda: None) is button
