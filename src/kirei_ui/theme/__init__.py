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
    qss_path = Path(path).expanduser()
    if qss_path.is_dir():
        raise IsADirectoryError(qss_path)
    return qss_path.read_text(encoding="utf-8")


def load_qss_dir(path: str | Path, recursive: bool = False) -> list[Path]:
    dir_path = Path(path).expanduser()
    if not dir_path.exists():
        raise FileNotFoundError(dir_path)
    if not dir_path.is_dir():
        raise NotADirectoryError(dir_path)

    pattern = "**/*.qss" if recursive else "*.qss"
    return sorted(p for p in dir_path.glob(pattern) if p.is_file())


def build_qss(
    theme: str | None = "base",
    qss_dirs: list[str | Path] | None = None,
    qss_files: list[str | Path] | None = None,
    recursive: bool = False,
    extra_qss: str | None = None,
) -> str:
    chunks: list[str] = []

    if theme is not None:
        builtin = load_builtin_qss(theme).strip()
        if builtin:
            chunks.append(builtin)

    for qss_dir in qss_dirs or []:
        for qss_file in load_qss_dir(qss_dir, recursive=recursive):
            dir_qss = load_qss_file(qss_file).strip()
            if dir_qss:
                chunks.append(dir_qss)

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
        qss_dirs: list[str | Path] | None = None,
        qss_files: list[str | Path] | None = None,
        recursive: bool = False,
        extra_qss: str | None = None,
    ) -> KireiStyle:
        return cls(
            build_qss(
                theme=theme,
                qss_dirs=qss_dirs,
                qss_files=qss_files,
                recursive=recursive,
                extra_qss=extra_qss,
            )
        )


class KireiTheme:
    @staticmethod
    def build(
        theme: str | None = "base",
        qss_dirs: list[str | Path] | None = None,
        qss_files: list[str | Path] | None = None,
        recursive: bool = False,
        extra_qss: str | None = None,
    ) -> str:
        return build_qss(
            theme=theme,
            qss_dirs=qss_dirs,
            qss_files=qss_files,
            recursive=recursive,
            extra_qss=extra_qss,
        )


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
    "load_qss_dir",
    "load_qss_file",
]
