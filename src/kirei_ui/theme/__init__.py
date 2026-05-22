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
    """Read a built-in theme's QSS by short name.

    Raises :class:`ValueError` if ``theme`` is not in
    :data:`BUILTIN_THEMES`.
    """
    try:
        theme_file = BUILTIN_THEMES[theme]
    except KeyError as exc:
        raise ValueError(f"Unknown builtin theme: {theme}") from exc

    return files("kirei_ui.resources.qss").joinpath(theme_file).read_text(encoding="utf-8")


def load_qss_file(path: str | Path) -> str:
    """Read a single QSS file and return its contents.

    ``~`` is expanded. Raises :class:`IsADirectoryError` if ``path``
    points to a directory; raises :class:`FileNotFoundError` if the
    file does not exist.
    """
    qss_path = Path(path).expanduser()
    if qss_path.is_dir():
        raise IsADirectoryError(qss_path)
    return qss_path.read_text(encoding="utf-8")


def load_qss_dir(path: str | Path, recursive: bool = False) -> list[Path]:
    """Return a sorted list of ``*.qss`` files in ``path``.

    Args:
        path: Directory to scan.
        recursive: When True, descend into subdirectories.

    Raises:
        FileNotFoundError: ``path`` does not exist.
        NotADirectoryError: ``path`` is not a directory.
    """
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
    """Compose a final stylesheet from a built-in theme plus user QSS.

    Sources are concatenated in this order, separated by blank lines:

    1. The built-in ``theme`` (when not ``None``).
    2. Every ``*.qss`` file inside each entry of ``qss_dirs`` (sorted,
       recursive when requested).
    3. Each file in ``qss_files``, in the given order.
    4. The ``extra_qss`` string, if provided.

    Empty / whitespace-only sources are skipped. Later sources can
    override earlier ones because Qt resolves QSS selectors with
    later rules taking precedence.
    """
    chunks: list[str] = []

    if theme is not None:
        builtin = load_builtin_qss(theme).strip()
        if builtin:
            chunks.append(builtin)

    for qss_dir in qss_dirs or []:
        for dir_qss_file in load_qss_dir(qss_dir, recursive=recursive):
            dir_qss = load_qss_file(dir_qss_file).strip()
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
    """Container for design-token style key/value pairs.

    Currently a thin wrapper around a ``dict``. Reserved for future
    token-based theming work; widgets do not consume it directly today.
    """

    values: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        """Return ``values[key]`` or ``default`` when missing."""
        return self.values.get(key, default)


@dataclass
class KireiStyle:
    """Pre-built QSS string with a constructor for the standard sources."""

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
        """Build a :class:`KireiStyle` by delegating to :func:`build_qss`."""
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
    """Static helper namespace for stylesheet composition.

    Today it only re-exports :func:`build_qss` under :meth:`build`.
    Reserved for future theme-management helpers.
    """

    @staticmethod
    def build(
        theme: str | None = "base",
        qss_dirs: list[str | Path] | None = None,
        qss_files: list[str | Path] | None = None,
        recursive: bool = False,
        extra_qss: str | None = None,
    ) -> str:
        """Static alias for :func:`build_qss`."""
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
