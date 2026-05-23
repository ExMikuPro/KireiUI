from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from importlib.resources import files
from pathlib import Path
from typing import Any

from kirei_ui.theme.loader import (
    BASE_QSS_MARKER,
    apply_base_qss,
    load_base_qss,
    load_default_tokens,
    load_tokens_file,
    merge_tokens,
    resolve_tokens,
)

BUILTIN_THEMES: dict[str, str] = {
    "base": "base.qss",
}


def load_builtin_qss(
    theme: str = "base",
    tokens: Mapping[str, Mapping[str, str]] | None = None,
) -> str:
    """Read a built-in theme's QSS by short name and resolve tokens.

    When ``tokens`` is ``None`` the bundled default token table is used.
    Raises :class:`ValueError` if ``theme`` is not in :data:`BUILTIN_THEMES`.
    """
    try:
        theme_file = BUILTIN_THEMES[theme]
    except KeyError as exc:
        raise ValueError(f"Unknown builtin theme: {theme}") from exc

    raw = files("kirei_ui.resources.qss").joinpath(theme_file).read_text(encoding="utf-8")
    return resolve_tokens(raw, tokens if tokens is not None else load_default_tokens())


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


def _collect_dir_tokens(qss_dirs: list[str | Path] | None) -> dict[str, dict[str, str]]:
    if not qss_dirs:
        return {}
    chunks: list[Mapping[str, Mapping[str, str]]] = []
    for qss_dir in qss_dirs:
        candidate = Path(qss_dir).expanduser() / "tokens.toml"
        if candidate.is_file():
            chunks.append(load_tokens_file(candidate))
    return merge_tokens(*chunks) if chunks else {}


def build_qss(
    theme: str | None = "base",
    qss_dirs: list[str | Path] | None = None,
    qss_files: list[str | Path] | None = None,
    recursive: bool = False,
    extra_qss: str | None = None,
    tokens: Mapping[str, Mapping[str, str]] | None = None,
) -> str:
    """Compose a final stylesheet from a built-in theme plus user QSS.

    Tokens come from the bundled defaults, are overridden by any
    ``tokens.toml`` found in ``qss_dirs`` (later dirs override earlier),
    and finally by ``tokens`` when provided. The resolved table is used
    to expand ``@group.key`` placeholders inside the built-in ``theme``.

    QSS sources are concatenated in this order, separated by blank lines:

    1. The built-in ``theme`` (when not ``None``), token-resolved.
    2. Every ``*.qss`` file inside each entry of ``qss_dirs`` (sorted,
       recursive when requested). ``tokens.toml`` files are skipped here
       because their contents are consumed as tokens, not appended QSS.
    3. Each file in ``qss_files``, in the given order.
    4. The ``extra_qss`` string, if provided.

    Empty / whitespace-only sources are skipped. Later sources can
    override earlier ones because Qt resolves QSS selectors with
    later rules taking precedence.
    """
    resolved_tokens = merge_tokens(
        load_default_tokens(),
        _collect_dir_tokens(qss_dirs),
        tokens or {},
    )

    chunks: list[str] = []

    if theme is not None:
        builtin = load_builtin_qss(theme, tokens=resolved_tokens).strip()
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

    Tokens are grouped (e.g. ``color``) so the same key can appear in
    different contexts. :meth:`from_file` parses a ``tokens.toml``;
    :meth:`as_mapping` returns the raw ``{group: {key: value}}`` dict
    used by :func:`build_qss`.
    """

    values: dict[str, dict[str, str]] = field(default_factory=dict)

    def get(self, group: str, key: str, default: Any = None) -> Any:
        """Return ``values[group][key]`` or ``default`` when missing."""
        return self.values.get(group, {}).get(key, default)

    def as_mapping(self) -> dict[str, dict[str, str]]:
        """Return the underlying ``{group: {key: value}}`` mapping."""
        return self.values

    @classmethod
    def from_file(cls, path: str | Path) -> KireiTokens:
        """Construct a :class:`KireiTokens` from a ``tokens.toml`` file."""
        return cls(load_tokens_file(path))

    @classmethod
    def defaults(cls) -> KireiTokens:
        """Return the bundled default token table."""
        return cls(load_default_tokens())


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
        tokens: Mapping[str, Mapping[str, str]] | None = None,
    ) -> KireiStyle:
        """Build a :class:`KireiStyle` by delegating to :func:`build_qss`."""
        return cls(
            build_qss(
                theme=theme,
                qss_dirs=qss_dirs,
                qss_files=qss_files,
                recursive=recursive,
                extra_qss=extra_qss,
                tokens=tokens,
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
        tokens: Mapping[str, Mapping[str, str]] | None = None,
    ) -> str:
        """Static alias for :func:`build_qss`."""
        return build_qss(
            theme=theme,
            qss_dirs=qss_dirs,
            qss_files=qss_files,
            recursive=recursive,
            extra_qss=extra_qss,
            tokens=tokens,
        )


__all__ = [
    "BASE_QSS_MARKER",
    "BUILTIN_THEMES",
    "KireiStyle",
    "KireiTheme",
    "KireiTokens",
    "_collect_dir_tokens",
    "apply_base_qss",
    "build_qss",
    "load_base_qss",
    "load_builtin_qss",
    "load_default_tokens",
    "load_qss_dir",
    "load_qss_file",
    "load_tokens_file",
    "merge_tokens",
    "resolve_tokens",
]
