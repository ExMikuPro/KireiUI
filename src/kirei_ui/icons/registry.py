from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import as_file, files
from pathlib import Path
from typing import Any, ClassVar


@dataclass(frozen=True)
class IconEntry:
    name: str
    style: str
    size: int
    file: str


class KireiIconRegistry:
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
        cls._loaded = False
        cls._entries = []
        cls._load()

    @classmethod
    def names(cls) -> list[str]:
        cls._load()
        return sorted({entry.name for entry in cls._entries})

    @classmethod
    def exists(cls, name: str, style: str = "regular", size: int = 20) -> bool:
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
