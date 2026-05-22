# KireiUI

![KireiUI Logo](https://github.com/ExMikuPro/KireiUI/blob/master/docs/Logo.png?raw=true)

KireiUI is a PySide6 / Qt6 fluent-style UI framework with chainable APIs, themeable QSS, and modular
widgets.

## Quick Start

```bash
pip install -e .
```

```python
from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.layout import KireiVStack
from kirei_ui.inputs import KireiButton

app = KireiApp()
root = KireiVStack().add(KireiButton("Hello"))
window = KireiWindow().title("KireiUI").size(800, 600).content(root)
window.show()
app.run()
```

## Build

Recommended (PEP 517/518):

```bash
python -m build
```

Legacy `setup.py` command:

```bash
python setup.py sdist bdist_wheel
```

Do not run `python setup.py` alone, because it requires a command and will report:
`error: no commands supplied`.

## Test

```bash
pytest
```

(`src` is configured in `pyproject.toml`, so no extra `PYTHONPATH` is needed.)
