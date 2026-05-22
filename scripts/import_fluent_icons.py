from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

PATTERN = re.compile(r"^ic_fluent_(?P<name>.+)_(?P<size>\d+)_(?P<style>regular|filled)\.svg$")


def snake_case(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Fluent UI SVG icons from local repo.")
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Local fluentui-system-icons dir",
    )
    parser.add_argument("--dest", type=Path, required=True, help="Destination fluent icon dir")
    parser.add_argument("--styles", nargs="+", default=["regular", "filled"])
    parser.add_argument("--sizes", nargs="+", type=int, default=[20, 24])
    return parser.parse_args()


def clean_output(dest: Path, styles: list[str]) -> None:
    for style in styles:
        target = dest / style
        target.mkdir(parents=True, exist_ok=True)
        for svg in target.glob("*.svg"):
            svg.unlink()


def copy_licenses(source: Path, dest: Path) -> None:
    for file_name in ["LICENSE", "NOTICE"]:
        src = source / file_name
        dst = dest / file_name
        if src.is_file():
            shutil.copy2(src, dst)
        else:
            print(f"[WARN] {file_name} not found at {src}")


def import_icons(
    source: Path,
    dest: Path,
    styles: list[str],
    sizes: list[int],
) -> list[dict[str, object]]:
    assets = source / "assets"
    if not assets.is_dir():
        raise FileNotFoundError(f"assets dir not found: {assets}")

    records: list[dict[str, object]] = []
    clean_output(dest, styles)

    for svg in sorted(assets.rglob("*.svg")):
        match = PATTERN.match(svg.name)
        if not match:
            continue

        style = match.group("style")
        size = int(match.group("size"))
        raw_name = match.group("name")

        if style not in styles or size not in sizes:
            continue

        name = snake_case(raw_name)
        filename = f"{name}_{size}_{style}.svg"
        relative = Path(style) / filename
        output = dest / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(svg, output)

        records.append(
            {
                "name": name,
                "style": style,
                "size": size,
                "file": str(relative).replace("\\", "/"),
            }
        )

    return records


def write_manifest(dest: Path, icons: list[dict[str, object]]) -> None:
    manifest = {
        "source": "microsoft/fluentui-system-icons",
        "version": None,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "icons": icons,
    }
    (dest / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()

    source = args.source.resolve()
    dest = args.dest.resolve()

    if not source.is_dir():
        raise FileNotFoundError(source)

    dest.mkdir(parents=True, exist_ok=True)

    styles = [snake_case(style) for style in args.styles]
    sizes = [int(size) for size in args.sizes]

    icons = import_icons(source, dest, styles, sizes)
    icons.sort(key=lambda item: (str(item["name"]), int(item["size"]), str(item["style"])))

    copy_licenses(source, dest)
    write_manifest(dest, icons)

    print(f"Imported {len(icons)} icons into {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
