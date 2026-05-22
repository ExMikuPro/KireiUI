from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

pytest.importorskip("PySide6")

from kirei_ui.app.application import KireiApp
from kirei_ui.app.window import KireiWindow
from kirei_ui.theme import build_qss, load_builtin_qss


def test_kirei_app_loads_base_qss_by_default() -> None:
    with patch("kirei_ui.app.application.QApplication.__init__", return_value=None), patch(
        "kirei_ui.app.application.KireiApp.setApplicationName"
    ), patch("kirei_ui.app.application.KireiApp.setOrganizationName"), patch(
        "kirei_ui.app.application.KireiApp.setStyleSheet"
    ) as mocked_set_style:
        KireiApp(argv=[])

    styled = mocked_set_style.call_args.args[0]
    assert "QPushButton[kirei=\"button\"]" in styled


def test_kirei_app_with_theme_none_skips_builtin() -> None:
    with TemporaryDirectory() as tmp:
        user_qss = Path(tmp) / "app.qss"
        user_qss.write_text("QLabel { color: #123456; }", encoding="utf-8")

        with patch("kirei_ui.app.application.QApplication.__init__", return_value=None), patch(
            "kirei_ui.app.application.KireiApp.setApplicationName"
        ), patch("kirei_ui.app.application.KireiApp.setOrganizationName"), patch(
            "kirei_ui.app.application.KireiApp.setStyleSheet"
        ) as mocked_set_style:
            KireiApp(argv=[], theme=None, qss_files=[user_qss])

    styled = mocked_set_style.call_args.args[0]
    assert "QPushButton[kirei=\"button\"]" not in styled
    assert "QLabel { color: #123456; }" in styled


def test_kirei_app_qss_files_appended_after_base() -> None:
    with TemporaryDirectory() as tmp:
        user_qss = Path(tmp) / "app.qss"
        user_qss.write_text("QWidget { background: #fafafa; }", encoding="utf-8")

        with patch("kirei_ui.app.application.QApplication.__init__", return_value=None), patch(
            "kirei_ui.app.application.KireiApp.setApplicationName"
        ), patch("kirei_ui.app.application.KireiApp.setOrganizationName"), patch(
            "kirei_ui.app.application.KireiApp.setStyleSheet"
        ) as mocked_set_style:
            KireiApp(argv=[], qss_files=[user_qss])

    styled = mocked_set_style.call_args.args[0]
    base_index = styled.find("QPushButton[kirei=\"button\"]")
    user_index = styled.find("QWidget { background: #fafafa; }")
    assert base_index != -1
    assert user_index != -1
    assert base_index < user_index


def test_load_qss_can_append() -> None:
    with TemporaryDirectory() as tmp:
        user_qss = Path(tmp) / "app.qss"
        user_qss.write_text("QLabel { color: #abcdef; }", encoding="utf-8")
        state = {"value": "QWidget { color: #111111; }"}

        def _set_style_sheet(value: str) -> None:
            state["value"] = value

        def _style_sheet() -> str:
            return state["value"]

        with patch("kirei_ui.app.application.QApplication.__init__", return_value=None), patch(
            "kirei_ui.app.application.KireiApp.setApplicationName"
        ), patch("kirei_ui.app.application.KireiApp.setOrganizationName"), patch(
            "kirei_ui.app.application.KireiApp.setStyleSheet", side_effect=_set_style_sheet
        ), patch("kirei_ui.app.application.KireiApp.styleSheet", side_effect=_style_sheet):
            app = KireiApp(argv=[], theme=None)
            app.load_qss(user_qss)

    assert "QWidget { color: #111111; }" in state["value"]
    assert "QLabel { color: #abcdef; }" in state["value"]


def test_set_theme_with_theme_none_uses_only_user_qss() -> None:
    with TemporaryDirectory() as tmp:
        user_qss = Path(tmp) / "app.qss"
        user_qss.write_text("QFrame { border: 1px solid #999; }", encoding="utf-8")
        state = {"value": ""}

        def _set_style_sheet(value: str) -> None:
            state["value"] = value

        with patch("kirei_ui.app.application.QApplication.__init__", return_value=None), patch(
            "kirei_ui.app.application.KireiApp.setApplicationName"
        ), patch("kirei_ui.app.application.KireiApp.setOrganizationName"), patch(
            "kirei_ui.app.application.KireiApp.setStyleSheet", side_effect=_set_style_sheet
        ):
            app = KireiApp(argv=[])
            app.set_theme(
                theme=None,
                qss_files=[user_qss],
                extra_qss="QPushButton { margin: 4px; }",
            )

    assert "QPushButton[kirei=\"button\"]" not in state["value"]
    assert "QFrame { border: 1px solid #999; }" in state["value"]
    assert "QPushButton { margin: 4px; }" in state["value"]


def test_kirei_window_no_longer_manages_qss() -> None:
    with patch("kirei_ui.app.window.QMainWindow.__init__", return_value=None), patch(
        "kirei_ui.app.window.KireiWindow.setWindowTitle"
    ) as mocked_title, patch("kirei_ui.app.window.KireiWindow.resize") as mocked_resize:
        KireiWindow()

    mocked_title.assert_called_once()
    mocked_resize.assert_called_once()


def test_build_qss_theme_none_still_builds_user_styles() -> None:
    with TemporaryDirectory() as tmp:
        qss_file = Path(tmp) / "u.qss"
        qss_file.write_text("QMenu { padding: 6px; }", encoding="utf-8")

        result = build_qss(theme=None, qss_files=[qss_file], extra_qss="QToolTip { color: #222; }")

    assert "QMenu { padding: 6px; }" in result
    assert "QToolTip { color: #222; }" in result


def test_load_builtin_qss_base_returns_qss() -> None:
    result = load_builtin_qss("base")
    assert "QPushButton[kirei=\"button\"]" in result
