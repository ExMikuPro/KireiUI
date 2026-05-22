# KireiUI API Reference

本文仅记录当前仓库**已实现且已导出的公开 API**（基于 `src/kirei_ui` 代码）。

## 导入建议

- 顶层导入：`from kirei_ui import ...`
- 分组导入（推荐）：`kirei_ui.app / inputs / layout / feedback / navigation / data / overlay / desktop / theme`

---

## KireiApp

### 说明
应用入口，负责 QApplication 生命周期与主题加载。

### 继承关系
`QApplication`

### 构造方法
```python
KireiApp(
    argv: list[str] | Sequence[str] | None = None,
    *,
    theme: str | None = "base",
    qss_dirs: list[str | Path] | None = None,
    qss_files: list[str | Path] | None = None,
    recursive: bool = False,
    extra_qss: str | None = None,
    enable_motion: bool = True,
    motion_duration: int = 180,
    application_name: str = "KireiUI App",
    organization_name: str = "KireiUI",
)
```

### 常用方法
- `set_theme(theme="base", qss_dirs=None, qss_files=None, recursive=False, extra_qss=None) -> Self`
- `theme(theme="base", qss_dirs=None, qss_files=None, recursive=False, extra_qss=None) -> Self`
- `load_qss(path: str | Path, append: bool = True) -> Self`
- `set_motion_enabled(value: bool = True) -> Self`
- `set_motion_duration(value: int = 180) -> Self`
- `run() -> int`

### QSS 样式控制
不直接设置组件样式；通过 `build_qss(...)` 构建并写入全局 styleSheet。

### 注意事项
`qss_dirs` 支持目录扫描，`recursive=True` 时递归子目录。

## KireiWindow

### 说明
主窗口封装，提供链式标题、尺寸和内容设置。

### 继承关系
`QMainWindow`

### 构造方法
```python
KireiWindow(
    *,
    title: str = "KireiUI",
    width: int = 1180,
    height: int = 760,
    parent: QWidget | None = None,
)
```

### 常用方法
- `title(text: str) -> Self`
- `size(width: int, height: int) -> Self` / `size() -> QSize`
- `content(widget: QWidget) -> Self`
- `set_content(widget: QWidget) -> None`
- `fixed_size(width: int, height: int) -> Self`
- `min_size(width: int, height: int) -> Self`
- `max_size(width: int, height: int) -> Self`
- `center() -> Self`
- `set_placeholder(text: str = "Hello KireiUI") -> None`

### QSS 样式控制
窗口内容组件样式由子组件 property + QSS 控制。

### 注意事项
- 构造方法所有参数均为关键字参数（`*`），位置传参会报错。
- `size()` 重载调用时，要么不传参数（返回 `QSize`），要么同时传 `width, height`（返回 `Self`）；只传一个会抛 `ValueError`。
- `set_placeholder()` 会用一个居中的占位 `QLabel` 替换中央组件，主要用于调试。

---

## 布局组件

### KireiHStack / KireiVStack
- 继承：`QWidget`
- 说明：水平/垂直堆叠容器
- 常用方法：`add`、`add_layout`、`spacing`、`padding`、`margins`、`stretch`、`clear`、`qt_layout`
- 样式控制：`kirei="hstack"` / `kirei="vstack"`

### KireiGrid
- 继承：`QWidget`
- 常用方法：`add_at`、`spacing`、`horizontal_spacing`、`vertical_spacing`、`padding`、`margins`、`clear`

### KireiForm
- 继承：`QWidget`
- 常用方法：`add_row(label, field)`、`spacing`、`padding`、`margins`、`clear`

### KireiScroll
- 继承：`QScrollArea`
- 常用方法：`content`、`resizable`、`horizontal_policy`、`vertical_policy`

### KireiPanel
- 继承：`QFrame`
- 常用方法：`content`、`padding`、`margins`、`variant`、`object_name`
- 样式控制：`kirei="panel"`，并设置 `kireiVariant`（兼容 `variant`）

### KireiSplitter
- 继承：`QSplitter`
- 常用方法：`horizontal()`、`vertical()`、`add()`、`sizes([...])`

### KireiStack
- 继承：`QStackedWidget`
- 常用方法：`add_page(name, widget)`、`current(name)`、`current_index(i)`、`page(name)`

### KireiTabs
- 继承：`QTabWidget`
- 常用方法：`add_tab`、`current_index`、`tabs_closable`

---

## 基础输入与文本

### KireiButton
- 继承：`QPushButton`
- 说明：按钮，支持 variant/size/loading/icon
- 构造：
```python
KireiButton(
    text: str = "",
    *,
    icon: str | QIcon | None = None,
    variant: ButtonVariant = "default",
    size: ButtonSize = "medium",
    icon_style: str = "regular",
    icon_size: int = 20,
    strict_icon: bool = False,
    parent: QWidget | None = None,
)
```
- `ButtonVariant`：`"default" | "primary" | "link" | "subtle" | "danger" | "warning"`
- `ButtonSize`：`"compact" | "medium"`
- 常用方法：`primary/default/link/subtle/danger/warning`、`compact/medium`、`loading`、`on_click`、`on_click_checked`、`icon`、`text`、`tooltip`、`enabled/disabled`、`checkable`、`checked`
- 样式控制：`kirei="button"`、`kireiVariant`、`kireiSize`、`kireiState`（兼容 `variant/size`）
- 注意：`loading(True)` 会禁用按钮并替换文本为"处理中..."。

### KireiLabel / KireiTitle / KireiText
- 继承：`QLabel`（Title/Text 继承 Label）
- 常用方法：`text`、`align_center/left/right`、`word_wrap`、`variant`、`role`
- 样式控制：`kireiRole`（`label/title/text`）+ `kireiVariant`

### KireiInput
- 继承：`QLineEdit`
- 常用方法：`placeholder`、`value`、`get_value`、`clearable`、`readonly`、`max_length`、`on_change`、`on_submit`
- 样式控制：`kirei="input"`、`kireiRole="input"`

### KireiPassword
- 继承：`KireiInput`
- 常用方法：`show_password`
- 样式控制：`kireiRole="password"`

### KireiTextarea
- 继承：`QTextEdit`
- 常用方法：`placeholder`、`value`、`get_value`、`readonly`、`on_change`
- 样式控制：`kirei="textarea"`、`kireiRole="textarea"`

### KireiCheckbox / KireiRadio
- 继承：`QCheckBox` / `QRadioButton`
- 常用方法：`text`、`checked`、`is_checked`、`on_change`
- 样式控制：`kirei="checkbox"|"radio"`，`kireiRole`

### KireiComboBox
- 继承：`QComboBox`
- 常用方法：`add_item`、`add_items`、`current`、`current_index`、`get_value`、`get_data`、`on_change`
- 样式控制：`kirei="combobox"`、`kireiRole="combobox"`

### KireiSwitch
- 继承：`QCheckBox + KireiMotionMixin`
- 常用方法：`checked`、`on_change`、`variant`、`size`
- 样式控制：`kirei="switch"`、`kireiVariant`、`kireiSize`

### KireiDivider
- 继承：`QFrame`
- 常用方法：`horizontal`、`vertical`、`variant`、`spacing`、`object_name`
- 样式控制：`kirei="divider"`、`kireiVariant`

---

## 数值与日期

### KireiSlider
- 继承：`QSlider`
- 方法：`horizontal`、`vertical`、`range`、`value/get_value`、`step`、`page_step`、`tick_position`、`on_change`

### KireiSpinBox / KireiDoubleSpinBox
- 继承：`QSpinBox` / `QDoubleSpinBox`
- 方法：`range`、`value/get_value`、`step`、`prefix`、`suffix`、`on_change`
- `KireiDoubleSpinBox` 额外：`decimals`

### KireiDateEdit / KireiTimeEdit / KireiDateTimeEdit
- 继承：`QDateEdit` / `QTimeEdit` / `QDateTimeEdit`
- 方法：`value/get_value`、`display_format`、`on_change`
- `DateEdit/DateTimeEdit` 额外：`calendar_popup`

---

## 反馈组件

### KireiAlert
- 继承：`QFrame`
- 方法：`title`、`description`、`variant/info/success/warning/danger`、`closable`、`on_close`

### KireiBadge
- 继承：`QLabel`
- 方法：`text`、`variant`、`default/primary/success/warning/danger/neutral`

### KireiTag
- 继承：`QFrame`
- 方法：`text`、`variant`、`default/primary/success/warning/danger`、`closable`、`on_close`

### KireiProgress
- 继承：`QProgressBar + KireiMotionMixin`
- 方法：`range`、`value/set_value`、`text_visible`、`indeterminate`、`variant/success/warning/danger`
- 样式控制：`kireiState="indeterminate"` 用于不确定态。

### KireiSpinner
- 继承：`QLabel`
- 方法：`text`、`start`、`stop`、`running`、`size`

### KireiEmpty
- 继承：`QWidget`
- 方法：`title`、`description`、`action`、`variant`

---

## 导航与结构扩展

### KireiCard
- 继承：`QFrame`
- 方法：`title`、`description`、`content`、`footer`、`variant`

### KireiSection
- 继承：`QFrame`
- 方法：`title`、`description`、`content`、`set_actions`

### KireiTopBar
- 继承：`QFrame`
- 方法：`title`、`leading`、`content`、`trailing`

### KireiNavItem
- 继承：`QPushButton`
- 方法：`text`、`key`、`selected`、`on_click`、`icon`、`get_key`
- 样式控制：`kireiState="selected|normal"`

### KireiSidebar
- 继承：`QFrame + KireiMotionMixin`
- 方法：`add_item`、`add_widget`、`current`、`on_change`、`collapse/expand/collapsed/toggle`
- 样式控制：`kireiState="expanded|collapsed"`

### KireiToolbar
- 继承：`QFrame`
- 方法：`add`、`add_action`、`separator`、`stretch`

### KireiBreadcrumbs
- 继承：`QFrame`
- 方法：`add_item`、`on_click`

### KireiActionGroup
- 继承：`QFrame`
- 方法：`add`、`spacing`

### KireiMenu
- 继承：`QMenu`
- 方法：`add_action`、`add_separator`、`popup_at`

---

## 数据展示

### KireiTable
- 继承：`QTableWidget`
- 方法：`columns`、`rows`、`add_row`、`clear_rows`、`selected_row`、`on_cell_click`

### KireiList
- 继承：`QListWidget`
- 方法：`add_item`、`add_items`、`current`、`get_value`、`on_change`

### KireiTree
- 继承：`QTreeWidget`
- 方法：`headers`、`add_item`、`clear_items`

### KireiSearchBox
- 继承：`KireiInput`
- 方法：`on_search`
- 样式控制：`kireiRole="searchBox"`

### KireiFilterBar
- 继承：`QWidget`
- 方法：`add_filter`、`add_action`、`clear_filters`

### KireiPagination
- 继承：`QWidget`
- 方法：`total`、`page`、`page_size`、`on_change`

---

## 弹层组件

### KireiDialog
- 继承：`QDialog + KireiMotionMixin`
- 方法：`title`、`content`、`footer`、`modal`、`show_animated`、`close_animated`、`open`

### KireiConfirm
- 继承：`QDialog + KireiMotionMixin`
- 方法：`title`、`description`、`confirm_text`、`cancel_text`、`on_confirm`、`on_cancel`、`open`

### KireiMessageBox
- 继承：`QMessageBox + KireiMotionMixin`
- 方法：`title`、`text`、`info/warning/danger`、`open`、`show_animated`、`close_animated`

### KireiDrawer
- 继承：`QDialog + KireiMotionMixin`
- 方法：`title`、`content`、`side`、`open`、`close`、`toggle`

### KireiPopover
- 继承：`QFrame + KireiMotionMixin`
- 方法：`content`、`popup_at`、`show_animated`、`close_animated`

### KireiTooltip
- 继承：`KireiMotionMixin`（工具类）
- 静态方法：`apply(widget, text)`、`show_animated(...)`、`show(...)`、`close_animated(...)`

---

## 桌面能力

### KireiAction
- 说明：对 `QAction` 的链式封装
- 方法：`text`、`icon`、`shortcut`、`tooltip`、`enabled/disabled`、`on_trigger`、`qt_action`

### KireiShortcut
- 方法：`on_trigger`、`enabled`

### KireiMenuBar
- 方法：`add_menu`、`add_action_to`

### KireiStatusBar
- 方法：`message`、`clear`、`add`

### KireiSystemTray
- 方法：`tooltip`、`show_tray`、`hide_tray`、`on_activate`

### KireiFileDialog / KireiColorDialog
- 静态方法：打开文件、保存文件、选目录、选颜色

---

## 图标与主题 API

### KireiIcon / icon(...)
- `KireiIcon.qicon(name, style="regular", size=20, strict=False)`
- `icon(...)` 为便捷函数

### KireiIconRegistry
- `names()`、`exists(...)`、`path(...)`、`resolve(...)`、`reload()`

### kirei_ui.theme
- `load_builtin_qss(theme="base") -> str`
- `load_qss_file(path: str | Path) -> str`
- `load_qss_dir(path: str | Path, recursive: bool = False) -> list[Path]`
- `build_qss(theme="base", qss_dirs=None, qss_files=None, recursive=False, extra_qss=None) -> str`
- `KireiTheme.build(...)` —— 与 `build_qss` 等价的类方法入口
- `KireiStyle.from_sources(...) -> KireiStyle` —— 返回带 `qss` 字段的样式对象
- `load_base_qss() -> str`、`apply_base_qss(force: bool = False) -> None` —— 直接对 `QApplication` 应用 base.qss，并保留可识别的 marker 以便覆写
- `BASE_QSS_MARKER`、`BUILTIN_THEMES`

---

## 实验性 / 未稳定 API

以下 API 已经导出，但当前实现非常薄、语义未稳定，使用前请关注后续变更：

- `KireiTokens`：`dataclass`，仅有 `values: dict[str, Any]` 与 `get(key, default=None)`，不要把它当作真正的 token 系统使用。后续会扩展为带语义层级的 token API。

---

## 计划中 / TODO（未作为稳定 API）

- 更系统化的 token API（目前 `KireiTokens` 仅为容器）
- 组件状态与语义尺寸的统一枚举常量
- 组件级文档注释（docstring）覆盖完善
