# KireiUI

![KireiUI Logo](docs/Logo.png)

KireiUI 是一个基于 PySide6 / Qt6 的轻量级桌面 UI 框架，通过链式 API 与 QSS 主题系统，帮助开发者快速构建结构清晰、风格统一的现代化界面。

## 项目定位

KireiUI 关注三件事：

- 用更少样板代码描述 UI 结构
- 用链式 API 提升组件组合效率
- 用 QSS 管理视觉风格并保持可维护性

核心边界：**Python 负责结构与行为，QSS 负责视觉风格。**

## 核心特性

- 基于 `PySide6 / Qt6`
- 链式 API（Fluent 风格）
- QSS 主题系统（内置 + 外部目录/文件 + 追加片段）
- 常用组件封装（输入、布局、反馈、导航、数据展示、弹层等）
- 统一设计规范（角色属性、语义状态、尺寸约定）
- 可运行示例代码

## 安装方式

### 1. 从源码安装

```bash
git clone https://github.com/ExMikuPro/KireiUI.git
cd KireiUI
pip install .
```

### 2. Editable 安装（推荐开发时）

```bash
pip install -e .
```

### 3. 安装依赖

运行时依赖：

```bash
pip install -r requirements.txt
```

开发依赖：

```bash
pip install -r requirements-dev.txt
```

## 快速开始

```python
from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.inputs import KireiButton
from kirei_ui.layout import KireiVStack

app = KireiApp()
root = KireiVStack().padding(16).add(KireiButton("Hello KireiUI").primary())
window = KireiWindow().title("KireiUI Quick Start").size(800, 480).content(root)
window.show()
app.run()
```

## 最小窗口示例

见 [examples/hello_window.py](examples/hello_window.py)：

```bash
python examples/hello_window.py
```

## Dashboard 示例

见 [examples/basic_dashboard.py](examples/basic_dashboard.py)：

```bash
python examples/basic_dashboard.py
```

## 项目目录结构

```text
KireiUI/
├─ src/kirei_ui/
│  ├─ app/              # KireiApp / KireiWindow
│  ├─ widgets/          # 组件实现
│  ├─ layout/           # 布局分组导出
│  ├─ inputs/           # 输入类组件分组导出
│  ├─ feedback/         # 反馈类组件分组导出
│  ├─ navigation/       # 导航类组件分组导出
│  ├─ data/             # 数据展示组件分组导出
│  ├─ desktop/          # 桌面特性组件分组导出
│  ├─ overlay/          # 弹层组件分组导出
│  ├─ theme/            # 主题构建与加载逻辑
│  ├─ motion/           # 动画能力
│  ├─ icons/            # Fluent 图标注册与加载
│  └─ resources/qss/    # 内置 base.qss
├─ styles/silicon_light/# 外置示例主题
├─ examples/            # 运行示例
├─ docs/                # 文档
└─ tests/               # 测试
```

## 当前已支持组件列表

- 应用层：`KireiApp`、`KireiWindow`
- 布局层：`KireiHStack`、`KireiVStack`、`KireiGrid`、`KireiForm`、`KireiScroll`、`KireiPanel`、`KireiSplitter`、`KireiStack`、`KireiTabs`
- 基础输入：`KireiButton`、`KireiInput`、`KireiPassword`、`KireiTextarea`、`KireiCheckbox`、`KireiRadio`、`KireiComboBox`、`KireiSwitch`
- 文本/分隔：`KireiLabel`、`KireiTitle`、`KireiText`、`KireiDivider`
- 反馈：`KireiAlert`、`KireiBadge`、`KireiTag`、`KireiProgress`、`KireiSpinner`、`KireiEmpty`
- 导航与结构：`KireiCard`、`KireiSection`、`KireiTopBar`、`KireiSidebar`、`KireiNavItem`、`KireiBreadcrumbs`、`KireiToolbar`、`KireiActionGroup`、`KireiMenu`
- 数据展示：`KireiTable`、`KireiList`、`KireiTree`、`KireiSearchBox`、`KireiFilterBar`、`KireiPagination`
- 弹层：`KireiDialog`、`KireiConfirm`、`KireiMessageBox`、`KireiDrawer`、`KireiPopover`、`KireiTooltip`
- 桌面能力：`KireiAction`、`KireiShortcut`、`KireiMenuBar`、`KireiStatusBar`、`KireiSystemTray`、`KireiFileDialog`、`KireiColorDialog`
- 数值/日期：`KireiSlider`、`KireiSpinBox`、`KireiDoubleSpinBox`、`KireiDateEdit`、`KireiTimeEdit`、`KireiDateTimeEdit`
- 图标：`KireiIcon`、`KireiIconRegistry`、`icon(...)`

## 主题系统简介

`KireiApp` 支持：

- `theme="base"` 加载内置 `base.qss`
- `qss_dirs=[...]` 批量加载目录下 `.qss`
- `qss_files=[...]` 指定文件加载
- `recursive=True` 递归扫描目录
- `extra_qss="..."` 追加临时样式片段

加载顺序：**内置主题 -> qss_dirs -> qss_files -> extra_qss**。

## 示例运行方式

下列示例自带 `sys.path` 引导，可在仓库根目录直接运行：

```bash
python examples/hello_window.py
python examples/basic_dashboard.py
python examples/form_example.py
python examples/theme_switching.py
python examples/qss_custom_theme.py
```

下列示例**需要先 `pip install -e .`** 才能找到 `kirei_ui` 包：

```bash
pip install -e .
python examples/basic_controls.py
python examples/component_gallery.py
python examples/kawaii_theme_demo.py
```

`components_gallery.py` 是 `component_gallery.py` 的转发脚本，并且依赖 `examples/` 作为 cwd，需要：

```bash
pip install -e .
cd examples
python components_gallery.py
```

更多见 [docs/EXAMPLES.md](docs/EXAMPLES.md)。

## 开发计划（Roadmap）

详见 [docs/ROADMAP.md](docs/ROADMAP.md)。

当前仍在开发中的方向包括：

- `Dialog / Toast / Tooltip / Menu / Table` 的更完整交互能力（部分已实现，仍在迭代）
- 主题 token 体系完善
- 组件画廊与文档站点
- 测试覆盖率提升

## 贡献指南

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## License

本项目采用 MIT License，见 [LICENSE](LICENSE)。

## 文档索引

- [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/API_REFERENCE.md](docs/API_REFERENCE.md)
- [docs/COMPONENTS.md](docs/COMPONENTS.md)
- [docs/THEMING.md](docs/THEMING.md)
- [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md)
- [docs/EXAMPLES.md](docs/EXAMPLES.md)
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [docs/icons.md](docs/icons.md)
