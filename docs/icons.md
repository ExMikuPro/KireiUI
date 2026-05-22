# Fluent Icons in KireiUI

KireiUI integrates selected SVG resources from **Microsoft Fluent UI System Icons**:
- Source: <https://github.com/microsoft/fluentui-system-icons>
- License: MIT

## Directory layout

- `src/kirei_ui/resources/icons/fluent/regular/`
- `src/kirei_ui/resources/icons/fluent/filled/`
- `src/kirei_ui/resources/icons/fluent/manifest.json`
- `src/kirei_ui/resources/icons/fluent/LICENSE`
- `src/kirei_ui/resources/icons/fluent/NOTICE`

## Import icons from local fluent repo

Use local clone only (no network download):

```bash
python scripts/import_fluent_icons.py \
  --source ../fluentui-system-icons \
  --dest src/kirei_ui/resources/icons/fluent \
  --styles regular filled \
  --sizes 20 24
```

The importer scans `source/assets` recursively and writes normalized files plus `manifest.json`.

## Runtime API

```python
from kirei_ui.icons import KireiIcon, KireiIconRegistry, icon

qicon = KireiIcon.qicon("add", style="regular", size=24)
exists = KireiIconRegistry.exists("add", style="regular", size=24)
```

- `strict=False` (default): missing icon returns empty `QIcon`.
- `strict=True`: missing icon raises `KeyError`.

## Button usage

```python
from kirei_ui.inputs import KireiButton

KireiButton("新增", icon="add")
KireiButton("完成").icon("checkmark_circle", style="filled", size=20)
```

## Notes

- `manifest.json` is the source of truth for lookup.
- If requested size/style is missing, registry will fallback predictably:
  - style: requested -> alternate (`regular` <-> `filled`)
  - size: nearest available size
