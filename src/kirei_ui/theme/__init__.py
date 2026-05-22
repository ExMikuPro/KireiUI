from __future__ import annotations

from dataclasses import dataclass, field
from importlib.resources import files
from pathlib import Path
from typing import Any

from kirei_ui.theme.loader import BASE_QSS_MARKER, apply_base_qss, load_base_qss

BUILTIN_THEMES: dict[str, str] = {
    "base": "base.qss",
}


def load_builtin_qss(theme: str = "base") -> str:
    try:
        theme_file = BUILTIN_THEMES[theme]
    except KeyError as exc:
        raise ValueError(f"Unknown builtin theme: {theme}") from exc

    return files("kirei_ui.resources.qss").joinpath(theme_file).read_text(encoding="utf-8")


def load_qss_file(path: str | Path) -> str:
    return Path(path).expanduser().read_text(encoding="utf-8")


def build_qss(
    theme: str | None = "base",
    qss_files: list[str | Path] | None = None,
    extra_qss: str | None = None,
) -> str:
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


@dataclass
class KireiTokens:
    values: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.values.get(key, default)


@dataclass
class KireiStyle:
    qss: str = ""

    @classmethod
    def from_sources(
        cls,
        theme: str | None = "base",
        qss_files: list[str | Path] | None = None,
        extra_qss: str | None = None,
    ) -> KireiStyle:
        return cls(build_qss(theme=theme, qss_files=qss_files, extra_qss=extra_qss))


class KireiTheme:
    @staticmethod
    def build(
        theme: str | None = "base",
        qss_files: list[str | Path] | None = None,
        extra_qss: str | None = None,
    ) -> str:
        return build_qss(theme=theme, qss_files=qss_files, extra_qss=extra_qss)


__all__ = [
    "BASE_QSS_MARKER",
    "BUILTIN_THEMES",
    "KireiStyle",
    "KireiTheme",
    "KireiTokens",
    "apply_base_qss",
    "build_qss",
    "load_base_qss",
    "load_builtin_qss",
    "load_qss_file",
]
