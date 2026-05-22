from __future__ import annotations

from importlib.resources import files
from pathlib import Path

BUILTIN_THEMES: dict[str, str] = {
    "base": "base.qss",
}


def load_builtin_qss(theme: str = "base") -> str:
    """Load a bundled KireiUI QSS theme by name."""
    try:
        theme_file = BUILTIN_THEMES[theme]
    except KeyError as exc:
        raise ValueError(f"Unknown builtin theme: {theme}") from exc

    return files("kirei_ui.resources.qss").joinpath(theme_file).read_text(encoding="utf-8")


def load_qss_file(path: str | Path) -> str:
    """Load a QSS file from user project path."""
    return Path(path).expanduser().read_text(encoding="utf-8")


def build_qss(
    theme: str | None = "base",
    qss_files: list[str | Path] | None = None,
    extra_qss: str | None = None,
) -> str:
    """Build final stylesheet content.

    Order: builtin theme first, then user qss files, then extra_qss.
    """
    chunks: list[str] = []

    if theme is not None:
        builtin = load_builtin_qss(theme).strip()
        if builtin:
            chunks.append(builtin)

    for qss_file in qss_files or []:
        user_qss = load_qss_file(qss_file).strip()
        if user_qss:
            chunks.append(user_qss)

    if extra_qss and extra_qss.strip():
        chunks.append(extra_qss.strip())

    return "\n\n".join(chunks)


__all__ = [
    "BUILTIN_THEMES",
    "build_qss",
    "load_builtin_qss",
    "load_qss_file",
]
