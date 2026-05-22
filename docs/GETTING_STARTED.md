# KireiUI 快速开始

## 1. 环境要求

- Python: `>=3.10`
- 操作系统: macOS / Windows / Linux
- Qt 绑定: `PySide6>=6.6.0`

## 2. 克隆项目

```bash
git clone https://github.com/ExMikuPro/KireiUI.git
cd KireiUI
```

## 3. 创建虚拟环境

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 4. 安装依赖

```bash
pip install -r requirements.txt
pip install -e .
```

开发模式建议：

```bash
pip install -r requirements-dev.txt
```

## 5. 运行第一个示例

```bash
python examples/hello_window.py
```

> 仓库内 `examples/` 下的脚本分三类：
>
> - 自带 `sys.path` 引导的脚本（如 `hello_window.py`、`basic_dashboard.py`、`form_example.py`、
    `theme_switching.py`、`qss_custom_theme.py`、`icon_demo.py`、`icon_browser.py`、`motion_demo.py`
    ），可在仓库根目录直接 `python examples/<name>.py` 运行。
> - **未带引导的脚本**（`basic_controls.py`、`component_gallery.py`、`kawaii_theme_demo.py`），需要先执行
    `pip install -e .`，之后用 `python examples/<name>.py` 运行。
> - **依赖 `examples/` 作为 cwd 的转发脚本**（`components_gallery.py`，仅做
    `from component_gallery import main`），运行时需
    `pip install -e . && cd examples && python components_gallery.py`。

## 6. 创建 KireiApp

```python
from kirei_ui.app import KireiApp

app = KireiApp(
    theme="base",
    qss_dirs=None,
    qss_files=None,
    recursive=False,
    extra_qss=None,
)
```

说明：

- `theme`: 内置主题名，当前内置 `base`
- `qss_dirs`: QSS 目录列表
- `qss_files`: QSS 文件列表
- `recursive`: 是否递归扫描 `qss_dirs`
- `extra_qss`: 额外样式字符串

## 7. 创建 KireiWindow

```python
from kirei_ui.app import KireiWindow

window = KireiWindow(title="KireiUI", width=960, height=640)
```

也可以链式：

```python
window = KireiWindow().title("KireiUI").size(960, 640)
```

## 8. 添加布局

```python
from kirei_ui.layout import KireiVStack

root = KireiVStack().padding(16).spacing(12)
window.content(root)
```

## 9. 添加按钮、标签、输入框

```python
from kirei_ui import KireiText, KireiTitle
from kirei_ui.inputs import KireiButton, KireiInput

root.add(KireiTitle("欢迎使用 KireiUI"))
root.add(KireiText("这是一个最小可运行示例"))
root.add(KireiInput().placeholder("请输入内容"))
root.add(KireiButton("提交").primary())
```

## 10. 加载 QSS 主题

目录方式：

```python
from pathlib import Path

app = KireiApp(
    qss_dirs=[Path("styles/silicon_light")],
    recursive=False,
)
```

文件方式：

```python
app = KireiApp(
    qss_files=["styles/silicon_light/01_base.qss"],
)
```

动态追加：

```python
app.load_qss("styles/silicon_light/99_overrides.qss", append=True)
```

## 11. 完整最小示例

```python
from kirei_ui import KireiTitle
from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.inputs import KireiButton, KireiInput
from kirei_ui.layout import KireiVStack


def main() -> int:
    app = KireiApp()
    root = (
        KireiVStack()
        .padding(20)
        .spacing(10)
        .add(KireiTitle("KireiUI Hello"))
        .add(KireiInput().placeholder("Type something"))
        .add(KireiButton("Submit").primary())
    )

    window = KireiWindow().title("KireiUI Demo").size(800, 480).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
```

## 12. 常见启动问题

1. `ModuleNotFoundError: No module named 'kirei_ui'`

- 先执行 `pip install -e .`
- 或确保在仓库根目录运行示例

2. Qt 平台插件错误（如 xcb）

- Linux 上安装系统 Qt 依赖（例如 `libxcb` 相关包）

3. UI 显示但样式不生效

- 检查 `qss_dirs` 路径是否存在
- 检查是否误传目录到 `qss_files`（会抛 `IsADirectoryError`）

4. 主题递归不生效

- 需要设置 `recursive=True`

## 13. macOS / Windows / Linux 注意事项

- macOS: 在 Retina 下窗口缩放正常由 Qt 接管，建议避免硬编码像素字体。
- Windows: PowerShell 激活 venv 命令与 bash 不同。
- Linux: 主题字体与渲染可能受桌面环境影响，建议在目标发行版实测 QSS。
