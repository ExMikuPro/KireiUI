from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from kirei_ui.app.application import KireiApp
from kirei_ui.app.window import KireiWindow
from kirei_ui.theme import build_qss, load_builtin_qss


def test_kirei_app_loads_base_qss_by_default() -> None:
    class _FakeApp:
        def __init__(self) -> None:
            self._style = ""

        def setStyleSheet(self, value: str) -> None:
            self._style = value

    app = _FakeApp()
    KireiApp.set_theme(app, theme="base")
    styled = app._style
    assert "QPushButton[kirei=\"button\"]" in styled


def test_kirei_app_with_theme_none_skips_builtin() -> None:
    with TemporaryDirectory() as tmp:
        user_qss = Path(tmp) / "app.qss"
        user_qss.write_text("QLabel { color: #123456; }", encoding="utf-8")

        class _FakeApp:
            def __init__(self) -> None:
                self._style = ""

            def setStyleSheet(self, value: str) -> None:
                self._style = value

        app = _FakeApp()
        KireiApp.set_theme(app, theme=None, qss_files=[user_qss])

    styled = app._style
    assert "QPushButton[kirei=\"button\"]" not in styled
    assert "QLabel { color: #123456; }" in styled


def test_kirei_app_qss_files_appended_after_base() -> None:
    with TemporaryDirectory() as tmp:
        user_qss = Path(tmp) / "app.qss"
        user_qss.write_text("QWidget { background: #fafafa; }", encoding="utf-8")

        class _FakeApp:
            def __init__(self) -> None:
                self._style = ""

            def setStyleSheet(self, value: str) -> None:
                self._style = value

        app = _FakeApp()
        KireiApp.set_theme(app, qss_files=[user_qss])

    styled = app._style
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

        class _FakeApp:
            def styleSheet(self) -> str:
                return _style_sheet()

            def setStyleSheet(self, value: str) -> None:
                _set_style_sheet(value)

        app = _FakeApp()
        KireiApp.load_qss(app, user_qss)

    assert "QWidget { color: #111111; }" in state["value"]
    assert "QLabel { color: #abcdef; }" in state["value"]


def test_set_theme_with_theme_none_uses_only_user_qss() -> None:
    with TemporaryDirectory() as tmp:
        user_qss = Path(tmp) / "app.qss"
        user_qss.write_text("QFrame { border: 1px solid #999; }", encoding="utf-8")
        state = {"value": ""}

        def _set_style_sheet(value: str) -> None:
            state["value"] = value

        class _FakeApp:
            def setStyleSheet(self, value: str) -> None:
                _set_style_sheet(value)

        app = _FakeApp()
        KireiApp.set_theme(
            app,
            theme=None,
            qss_files=[user_qss],
            extra_qss="QPushButton { margin: 4px; }",
        )

    assert "QPushButton[kirei=\"button\"]" not in state["value"]
    assert "QFrame { border: 1px solid #999; }" in state["value"]
    assert "QPushButton { margin: 4px; }" in state["value"]


def test_kirei_window_no_longer_manages_qss() -> None:
    QApplication.instance() or QApplication([])
    window = KireiWindow()
    assert window.windowTitle() == "KireiUI"


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


def test_build_qss_loads_qss_dirs_before_qss_files_and_sorted() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        qss_dir = root / "styles"
        qss_dir.mkdir()
        (qss_dir / "02_layout.qss").write_text("QWidget { padding: 1px; }", encoding="utf-8")
        (qss_dir / "01_base.qss").write_text("QWidget { margin: 1px; }", encoding="utf-8")
        file_qss = root / "app.qss"
        file_qss.write_text("QWidget { color: #111; }", encoding="utf-8")

        result = build_qss(theme=None, qss_dirs=[qss_dir], qss_files=[file_qss])

    idx_base = result.find("margin: 1px")
    idx_layout = result.find("padding: 1px")
    idx_file = result.find("color: #111")
    assert idx_base != -1
    assert idx_layout != -1
    assert idx_file != -1
    assert idx_base < idx_layout < idx_file


def test_build_qss_qss_dirs_recursive() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        qss_dir = root / "styles"
        nested = qss_dir / "nested"
        nested.mkdir(parents=True)
        (nested / "01_nested.qss").write_text("QLabel { font-size: 12px; }", encoding="utf-8")

        no_recursive = build_qss(theme=None, qss_dirs=[qss_dir], recursive=False)
        recursive = build_qss(theme=None, qss_dirs=[qss_dir], recursive=True)

    assert "font-size: 12px" not in no_recursive
    assert "font-size: 12px" in recursive


def test_build_qss_raises_for_invalid_dirs_and_files() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        missing_dir = root / "missing"
        not_dir = root / "not_dir.qss"
        not_dir.write_text("QLabel{}", encoding="utf-8")
        real_dir = root / "styles"
        real_dir.mkdir()

        with pytest.raises(FileNotFoundError):
            build_qss(theme=None, qss_dirs=[missing_dir])

        with pytest.raises(NotADirectoryError):
            build_qss(theme=None, qss_dirs=[not_dir])

        with pytest.raises(IsADirectoryError):
            build_qss(theme=None, qss_files=[real_dir])
