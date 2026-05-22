from __future__ import annotations

from importlib.resources import files

from PySide6.QtWidgets import QApplication

BASE_QSS_MARKER = "/* KireiUI base.qss */"
_BASE_QSS_END_MARKER = "/* /KireiUI base.qss */"


def load_base_qss() -> str:
    """Load the bundled base.qss content."""
    base_qss = files("kirei_ui.resources.qss").joinpath("base.qss").read_text(encoding="utf-8")
    return f"{BASE_QSS_MARKER}\n{base_qss.rstrip()}\n{_BASE_QSS_END_MARKER}"


def _strip_managed_base_qss(style_sheet: str) -> str:
    start = style_sheet.find(BASE_QSS_MARKER)
    if start == -1:
        return style_sheet

    end = style_sheet.find(_BASE_QSS_END_MARKER, start)
    if end == -1:
        return style_sheet.replace(BASE_QSS_MARKER, "", 1).strip()

    end += len(_BASE_QSS_END_MARKER)
    return (style_sheet[:start] + style_sheet[end:]).strip()


def apply_base_qss(force: bool = False) -> None:
    """Apply base.qss to QApplication if available.

    The base stylesheet is prepended so user-provided app styles can override it.
    """
    app = QApplication.instance()
    if app is None:
        return

    current = app.styleSheet() or ""
    if (BASE_QSS_MARKER in current) and not force:
        return

    user_styles = _strip_managed_base_qss(current)
    base_styles = load_base_qss()

    if user_styles:
        app.setStyleSheet(f"{base_styles}\n\n{user_styles}")
    else:
        app.setStyleSheet(base_styles)
