# KireiUI 组件手册

本手册面向“怎么用”，不是完整 API 表。完整签名见 `docs/API_REFERENCE.md`。

## Button（KireiButton）

### 什么时候使用

- 触发动作（提交、保存、删除、打开弹窗）

### 什么时候不要使用

- 纯文本导航（优先用 `KireiNavItem` / `KireiBreadcrumbs`）

### 基础示例

```python
from kirei_ui.inputs import KireiButton

primary = KireiButton("保存").primary()
secondary = KireiButton("取消").default()
danger = KireiButton("删除").danger()
link = KireiButton("查看详情").link()
```

### 组合示例

```python
from kirei_ui.layout import KireiHStack

actions = (
    KireiHStack()
    .spacing(8)
    .add(KireiButton("取消").subtle())
    .add(KireiButton("提交").primary())
)
```

### 样式建议

- 使用 `kireiVariant` 控制语义，避免 Python 写颜色

### 可访问性建议

- 文案尽量动词开头（如“保存设置”）

### 常见错误

- 把 `danger` 用在非破坏操作

## Text / Title / Label

- `KireiTitle`：页面或区块主标题
- `KireiText`：正文说明
- `KireiLabel`：字段标签、辅助说明

常见错误：把纯装饰文本当标题，导致信息层级混乱。

## Input / Password / Textarea

### 使用建议

- `KireiInput`：单行短文本
- `KireiPassword`：密码输入
- `KireiTextarea`：长文本

### 示例

```python
from kirei_ui.inputs import KireiInput, KireiPassword, KireiTextarea

username = KireiInput().placeholder("用户名").clearable()
password = KireiPassword().placeholder("密码")
bio = KireiTextarea().placeholder("个人简介")
```

常见错误：用 `Textarea` 输入短 ID，导致交互冗余。

## Checkbox / Radio

- `Checkbox`: 多选或布尔开关
- `Radio`: 互斥单选（需在同一父容器内组织）

常见错误：只有两个互斥状态时还用多个 checkbox。

## ComboBox

适合固定候选项选择。

```python
from kirei_ui.inputs import KireiComboBox

role = KireiComboBox().add_items(["User", "Admin", "Guest"]).current("User")
```

## Divider

用于分隔区域，不要用于制造“视觉空白”（空白应由 layout spacing/margins 提供）。

## Panel

轻量容器，适合包裹一个主内容区。

```python
from kirei_ui.layout import KireiPanel

panel = KireiPanel().variant("default").content(form_widget)
```

## Tabs / Stack

- `KireiTabs`: 用户可见 tab 切换
- `KireiStack`: 程序控制页面切换

## Card / Section

- `KireiCard`: 信息块 + 标题 / 描述 / 内容 / footer，独立成块
- `KireiSection`: 区域切分（标题 + 描述 + 操作栏 + 内容），适合页面内多模块组织

```python
from PySide6.QtWidgets import QWidget
from kirei_ui.layout import KireiCard, KireiSection

card = KireiCard().title("Quick Filters").description("最近活跃数据").content(QWidget())
section = KireiSection().title("最近活动").description("过去 7 天").content(QWidget())
```

## Tooltip / Popover / Drawer / Dialog

- `KireiTooltip`：纯静态工具类，对任意 `QWidget` 调用 `KireiTooltip.apply(widget, "text")` 即可挂提示文案
- `KireiPopover`：轻量浮层，`popup_at(anchor)` 锚定到目标控件
- `KireiDrawer`：从屏幕一侧滑入的抽屉，`side("left" | "right" | "top" | "bottom")`
- `KireiDialog` / `KireiConfirm` / `KireiMessageBox`：模态弹窗，含 fade-in / fade-out 动画

```python
from kirei_ui.inputs import KireiButton
from kirei_ui.overlay import KireiTooltip

icon_btn = KireiButton().icon("settings")
KireiTooltip.apply(icon_btn, "设置")
```

## Form

适合标签 + 字段的结构化录入。

```python
from kirei_ui.layout import KireiForm

form = KireiForm().add_row("用户名", username).add_row("密码", password)
```

## Scroll

内容高度不确定时使用。

## 反馈组件（Alert/Badge/Tag/Progress/Spinner/Empty）

- Alert：上下文提示
- Badge/Tag：轻量状态标记
- Progress/Spinner：加载或进度
- Empty：空状态页

## 可访问性通用建议

- 保证文本与背景对比度
- 为图标按钮添加 tooltip
- 不仅用颜色区分状态，配合文案/图标

## 常见组合模式

1. 表单页：`TopBar + Card + Form + Action Buttons`
2. 数据页：`FilterBar + Table/List + Pagination`
3. 设置页：`Sidebar + Stack/Tabs + Panel`

## 计划中 / TODO

- `KireiButton` 的标准化 loading 指示器（当前有 loading 状态，但非图形 spinner）
- 更系统的可访问性辅助能力（键盘导航提示等）
