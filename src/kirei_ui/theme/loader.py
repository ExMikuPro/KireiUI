from __future__ import annotations

import re
import sys
from collections.abc import Mapping
from importlib.resources import files
from pathlib import Path

from PySide6.QtWidgets import QApplication

if sys.version_info >= (3, 11):
    import tomllib as _toml
else:  # pragma: no cover - <3.11 fallback
    import tomli as _toml  # type: ignore[no-redef]

BASE_QSS_MARKER = "/* KireiUI base.qss */"
_BASE_QSS_END_MARKER = "/* /KireiUI base.qss */"

_TOKEN_PATTERN = re.compile(r"@([a-zA-Z][\w]*)\.([a-zA-Z_][\w]*)")


def load_default_tokens() -> dict[str, dict[str, str]]:
    """Return the bundled default token table (silicon_light palette)."""
    raw = files("kirei_ui.resources.qss").joinpath("tokens.toml").read_bytes()
    return _normalise_tokens(_toml.loads(raw.decode("utf-8")))


def load_tokens_file(path: str | Path) -> dict[str, dict[str, str]]:
    """Read a ``tokens.toml`` from disk into a normalised token table."""
    text = Path(path).expanduser().read_text(encoding="utf-8")
    return _normalise_tokens(_toml.loads(text))


def merge_tokens(
    *sources: Mapping[str, Mapping[str, str]],
) -> dict[str, dict[str, str]]:
    """Merge token tables left-to-right; later sources override earlier ones."""
    merged: dict[str, dict[str, str]] = {}
    for src in sources:
        for group, items in src.items():
            bucket = merged.setdefault(group, {})
            bucket.update(items)
    return merged


def resolve_tokens(qss: str, tokens: Mapping[str, Mapping[str, str]]) -> str:
    """Substitute ``@group.key`` placeholders in ``qss`` with values from ``tokens``.

    Raises :class:`KeyError` listing every unknown placeholder so missing
    tokens fail loudly rather than silently rendering empty strings.
    """
    missing: set[str] = set()

    def _sub(match: re.Match[str]) -> str:
        group, key = match.group(1), match.group(2)
        try:
            return tokens[group][key]
        except KeyError:
            missing.add(f"@{group}.{key}")
            return match.group(0)

    rendered = _TOKEN_PATTERN.sub(_sub, qss)
    if missing:
        raise KeyError(
            "Unresolved QSS tokens: " + ", ".join(sorted(missing))
        )
    return rendered


def load_base_qss(tokens: Mapping[str, Mapping[str, str]] | None = None) -> str:
    """Load the bundled base.qss and resolve token placeholders.

    When ``tokens`` is ``None`` the bundled default token table is used,
    so the base stylesheet always renders cleanly.
    """
    base_qss = files("kirei_ui.resources.qss").joinpath("base.qss").read_text(encoding="utf-8")
    resolved = resolve_tokens(base_qss, tokens if tokens is not None else load_default_tokens())
    return f"{BASE_QSS_MARKER}\n{resolved.rstrip()}\n{_BASE_QSS_END_MARKER}"


def _normalise_tokens(
    raw: Mapping[str, object],
) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for group, items in raw.items():
        if not isinstance(items, Mapping):
            continue
        out[group] = {str(k): str(v) for k, v in items.items()}
    return out


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
    if not isinstance(app, QApplication):
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
