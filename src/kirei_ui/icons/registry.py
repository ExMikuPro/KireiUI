from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import as_file, files
from pathlib import Path
from typing import Any, ClassVar


@dataclass(frozen=True)
class IconEntry:
    """One entry in the icon manifest.

    Attributes:
        name: Logical icon name (e.g. ``"save"``).
        style: ``"regular"`` or ``"filled"``.
        size: Native pixel size of the bundled SVG.
        file: Path of the SVG relative to ``resources/icons/fluent/``.
    """

    name: str
    style: str
    size: int
    file: str


class KireiIconRegistry:
    """Bundled Fluent icon registry, loaded lazily from ``manifest.json``.

    The registry caches the parsed manifest on the class itself, so the
    JSON file is read once per process. Use :meth:`reload` after
    swapping the bundled manifest at runtime (rarely needed).
    """

    _loaded: ClassVar[bool] = False
    _entries: ClassVar[list[IconEntry]] = []

    @classmethod
    def _load(cls) -> None:
        if cls._loaded:
            return

        manifest_resource = files("kirei_ui").joinpath("resources/icons/fluent/manifest.json")
        with manifest_resource.open("r", encoding="utf-8") as handle:
            payload: dict[str, Any] = json.load(handle)

        entries: list[IconEntry] = []
        for item in payload.get("icons", []):
            entries.append(
                IconEntry(
                    name=str(item["name"]),
                    style=str(item["style"]),
                    size=int(item["size"]),
                    file=str(item["file"]),
                )
            )

        cls._entries = entries
        cls._loaded = True

    @classmethod
    def reload(cls) -> None:
        """Drop the cached manifest and reload it from disk on next access."""
        cls._loaded = False
        cls._entries = []
        cls._load()

    @classmethod
    def names(cls) -> list[str]:
        """Return all known icon names, deduplicated and sorted."""
        cls._load()
        return sorted({entry.name for entry in cls._entries})

    @classmethod
    def exists(cls, name: str, style: str = "regular", size: int = 20) -> bool:
        """Return True when an entry can be resolved for the requested combination."""
        return cls.resolve(name, style=style, size=size) is not None

    @classmethod
    def path(
        cls,
        name: str,
        style: str = "regular",
        size: int = 20,
        *,
        strict: bool = False,
    ) -> str | None:
        """Return a filesystem path to the resolved icon SVG.

        Args:
            name: Icon name to resolve.
            style: Preferred style — ``"regular"`` or ``"filled"``.
            size: Preferred pixel size; the closest available size is chosen.
            strict: When True, raise :class:`KeyError` if no entry matches.
                Default returns ``None``.

        Returns:
            Filesystem path as a string, or ``None`` when the icon is missing
            (only when ``strict`` is False).
        """
        entry = cls.resolve(name, style=style, size=size)
        if entry is None:
            if strict:
                raise KeyError(f"Icon not found: name={name}, style={style}, size={size}")
            return None

        resource = files("kirei_ui").joinpath(f"resources/icons/fluent/{entry.file}")
        with as_file(resource) as extracted:
            return str(Path(extracted))

    @classmethod
    def resolve(cls, name: str, style: str = "regular", size: int = 20) -> IconEntry | None:
        """Resolve ``(name, style, size)`` to the best-matching :class:`IconEntry`.

        Matching prefers exact ``style`` first, then the alternate
        style, then any style. Within each candidate style, an exact
        size match is preferred; otherwise the size with the smallest
        absolute delta wins. Returns ``None`` when no entry matches the
        name at all.
        """
        cls._load()

        normalized_name = name.strip().lower()
        normalized_style = style.strip().lower()
        target_size = int(size)

        by_name = [entry for entry in cls._entries if entry.name == normalized_name]
        if not by_name:
            return None

        preferred_styles = [normalized_style]
        if normalized_style == "regular":
            preferred_styles.append("filled")
        elif normalized_style == "filled":
            preferred_styles.append("regular")

        for candidate_style in preferred_styles:
            by_style = [entry for entry in by_name if entry.style == candidate_style]
            if not by_style:
                continue

            exact = [entry for entry in by_style if entry.size == target_size]
            if exact:
                return exact[0]

            by_style.sort(key=lambda entry: abs(entry.size - target_size))
            return by_style[0]

        by_name.sort(key=lambda entry: (entry.style, abs(entry.size - target_size)))
        return by_name[0]
