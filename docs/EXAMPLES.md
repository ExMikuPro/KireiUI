# KireiUI 示例说明

## 1) hello_window.py

用途说明：最小窗口 + 标题 + 按钮。

运行命令：

```bash
python3 examples/hello_window.py
```

完整代码：

```python
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from kirei_ui import KireiTitle
from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.inputs import KireiButton
from kirei_ui.layout import KireiVStack


def _theme_dirs() -> list[Path]:
    theme = ROOT / "styles" / "silicon_light"
    return [theme] if theme.is_dir() else []


def main() -> int:
    app = KireiApp(qss_dirs=_theme_dirs() or None)

    root = (
        KireiVStack()
        .padding(24)
        .spacing(12)
        .add(KireiTitle("Hello KireiUI"))
        .add(KireiButton("Click Me").primary().on_click(lambda: print("clicked")))
    )

    window = KireiWindow().title("KireiUI Hello").size(720, 420).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
```

预期效果说明：显示一个带标题与 primary 按钮的窗口。

涉及组件：`KireiApp`、`KireiWindow`、`KireiVStack`、`KireiTitle`、`KireiButton`。

## 2) basic_dashboard.py

用途说明：典型工具型后台布局（TopBar + Sidebar + Card + Table + Pagination）。

运行命令：

```bash
python3 examples/basic_dashboard.py
```

完整代码：

```python
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from kirei_ui import KireiText, KireiTitle
from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.data import KireiPagination, KireiTable
from kirei_ui.inputs import KireiButton, KireiInput
from kirei_ui.layout import KireiCard, KireiForm, KireiHStack, KireiVStack
from kirei_ui.navigation import KireiSidebar, KireiTopBar


def _theme_dirs() -> list[Path]:
    theme = ROOT / "styles" / "silicon_light"
    return [theme] if theme.is_dir() else []


def main() -> int:
    app = KireiApp(qss_dirs=_theme_dirs() or None)

    sidebar = (
        KireiSidebar()
        .add_item("Overview", "overview")
        .add_item("Projects", "projects")
        .add_item("Settings", "settings")
        .current("overview")
    )

    table = (
        KireiTable()
        .columns(["Name", "Status", "Owner"])
        .rows([
            ["KireiUI", "Active", "Siling"],
            ["Desktop App", "Paused", "Miku"],
            ["Theme Pack", "Active", "Team"],
        ])
    )

    root = (
        KireiVStack()
        .padding(16)
        .spacing(12)
        .add(KireiTopBar("KireiUI Dashboard").trailing(KireiButton("New").primary()))
        .add(
            KireiHStack()
            .spacing(12)
            .add(sidebar)
            .add(
                KireiVStack()
                .spacing(12)
                .add(
                    KireiCard()
                    .title("Quick Filters")
                    .description("Simple dashboard filter form")
                    .content(
                        KireiForm()
                        .add_row("Keyword", KireiInput().placeholder("Search..."))
                        .add_row("Owner", KireiInput().placeholder("Owner"))
                    )
                )
                .add(KireiCard().title("Projects").content(table))
                .add(
                    KireiHStack()
                    .spacing(8)
                    .add(KireiText("Use pagination to navigate data."))
                    .add(KireiPagination().total(128).page_size(10).page(1))
                )
            )
        )
    )

    window = KireiWindow().title("KireiUI Dashboard").size(1200, 820).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
```

预期效果说明：左侧导航 + 右侧过滤与列表区域。

涉及组件：`KireiTopBar`、`KireiSidebar`、`KireiCard`、`KireiForm`、`KireiTable`、`KireiPagination`。

## 3) form_example.py

用途说明：标准表单录入结构。

运行命令：

```bash
python3 examples/form_example.py
```

完整代码：

```python
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from kirei_ui import KireiTitle
from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.inputs import KireiButton, KireiCheckbox, KireiComboBox, KireiInput, KireiPassword
from kirei_ui.layout import KireiForm, KireiHStack, KireiVStack


def _theme_dirs() -> list[Path]:
    theme = ROOT / "styles" / "silicon_light"
    return [theme] if theme.is_dir() else []


def main() -> int:
    app = KireiApp(qss_dirs=_theme_dirs() or None)

    name = KireiInput().placeholder("Username")
    pwd = KireiPassword().placeholder("Password")
    role = KireiComboBox().add_items(["User", "Admin", "Guest"]).current("User")

    root = (
        KireiVStack()
        .padding(24)
        .spacing(12)
        .add(KireiTitle("Form Example"))
        .add(
            KireiForm()
            .spacing(10)
            .add_row("Username", name)
            .add_row("Password", pwd)
            .add_row("Role", role)
            .add_row("Remember", KireiCheckbox("Enable"))
        )
        .add(
            KireiHStack()
            .stretch()
            .add(KireiButton("Cancel").subtle())
            .add(KireiButton("Submit").primary())
        )
    )

    window = KireiWindow().title("KireiUI Form Example").size(900, 560).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
```

预期效果说明：用户名/密码/角色/记住我字段 + 操作按钮。

涉及组件：`KireiForm`、`KireiInput`、`KireiPassword`、`KireiCheckbox`、`KireiComboBox`、`KireiButton`。

## 4) theme_switching.py

用途说明：运行时切换 `base` 与 `styles/silicon_light`。

运行命令：

```bash
python3 examples/theme_switching.py
```

完整代码：

```python
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from kirei_ui import KireiText, KireiTitle
from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.inputs import KireiButton
from kirei_ui.layout import KireiCard, KireiHStack, KireiVStack


def main() -> int:
    theme_dir = ROOT / "styles" / "silicon_light"

    app = KireiApp()

    status = KireiText("Current theme: base")

    def use_builtin() -> None:
        app.set_theme(theme="base")
        status.text("Current theme: base")

    def use_silicon() -> None:
        app.set_theme(theme=None, qss_dirs=[theme_dir] if theme_dir.is_dir() else None)
        status.text("Current theme: styles/silicon_light")

    root = (
        KireiVStack()
        .padding(24)
        .spacing(12)
        .add(KireiTitle("Theme Switching Demo"))
        .add(status)
        .add(
            KireiCard()
            .title("Actions")
            .content(
                KireiHStack()
                .spacing(8)
                .add(KireiButton("Use Base Theme").on_click(use_builtin))
                .add(KireiButton("Use Silicon Theme").primary().on_click(use_silicon))
            )
        )
    )

    window = KireiWindow().title("KireiUI Theme Switching").size(880, 520).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
```

预期效果说明：点击按钮后调用 `app.set_theme(...)` 并更新状态文本。

涉及组件：`KireiApp.set_theme`、`KireiCard`、`KireiButton`。

## 5) components_gallery.py / component_gallery.py

用途说明：综合组件展示页。`component_gallery.py` 是真正的实现，`components_gallery.py` 是一个仅做 `from component_gallery import main` 的转发脚本。

> 这两个脚本**未内置 `sys.path` 引导**，运行约束如下：
>
> - `component_gallery.py`：先 `pip install -e .`，之后可在仓库任意目录用 `python examples/component_gallery.py` 运行。
> - `components_gallery.py`：除了 `pip install -e .`，还**必须把 `examples/` 当作 cwd**（因为它对 `component_gallery` 做 sibling import），否则会报 `ModuleNotFoundError: No module named 'component_gallery'`。

运行命令：

```bash
pip install -e .

# 推荐：直接运行真正的实现
python examples/component_gallery.py

# 或：进入 examples/ 再运行转发脚本
cd examples
python components_gallery.py
```

`components_gallery.py` 完整代码：

```python
from component_gallery import main


if __name__ == "__main__":
    raise SystemExit(main())
```

预期效果说明：打开综合组件展示页面。

涉及组件：输入、反馈、导航、弹层、数据展示、桌面能力。

## 6) qss_custom_theme.py

用途说明：演示 `theme + qss_files + extra_qss` 组合覆盖。

运行命令：

```bash
python3 examples/qss_custom_theme.py
```

完整代码：

```python
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from kirei_ui import KireiText, KireiTitle
from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.inputs import KireiButton, KireiInput
from kirei_ui.layout import KireiCard, KireiVStack


def main() -> int:
    style_file = ROOT / "styles" / "silicon_light" / "99_overrides.qss"

    app = KireiApp(
        theme="base",
        qss_files=[style_file] if style_file.is_file() else None,
        extra_qss='QPushButton[kirei="button"] { min-height: 36px; }',
    )

    root = (
        KireiVStack()
        .padding(20)
        .spacing(12)
        .add(KireiTitle("QSS Custom Theme Demo"))
        .add(KireiText("This demo combines base theme + local qss file + extra_qss."))
        .add(
            KireiCard()
            .title("Form")
            .content(
                KireiVStack()
                .spacing(8)
                .add(KireiInput().placeholder("Your name"))
                .add(KireiButton("Submit").primary())
            )
        )
    )

    window = KireiWindow().title("KireiUI QSS Theme").size(920, 580).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
```

预期效果说明：加载 base 主题后叠加本地 QSS 与临时样式片段。

涉及组件：`KireiApp`、`KireiVStack`、`KireiCard`、`KireiInput`、`KireiButton`。

## 7) 仓库已有扩展示例

- [basic_controls.py](../examples/basic_controls.py)
- [component_gallery.py](../examples/component_gallery.py)
- [motion_demo.py](../examples/motion_demo.py)
- [icon_demo.py](../examples/icon_demo.py)
- [icon_browser.py](../examples/icon_browser.py)
- [kawaii_theme_demo.py](../examples/kawaii_theme_demo.py)
