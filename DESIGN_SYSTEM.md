# KireiUI Design System 规范

## 1) 视觉风格基线
- KireiUI 视觉风格参考 Atlassian AUI 与 Elastic EUI。
- 整体定位为企业级后台 UI：干净、克制、信息密度适中。
- 组件状态要清晰可辨：`hover`、`pressed`、`disabled`、`focus`。
- 语义变体要统一：`primary`、`danger`、`warning`、`success` 等。

## 2) 组件 API 风格
- 组件 API 使用链式 Fluent API。
- 典型调用风格：
  - `KireiButton("Submit").primary().compact().on_click(...)`
  - `KireiInput().placeholder("Enter username").readonly()`

## 3) Python 职责边界
Python 代码只负责：
- 组件封装
- 链式 API
- 组件行为（如 signal 绑定、输入输出）
- 组件状态（enabled/disabled/loading 等）
- 设置 QSS property（`setProperty(...)`）
- 组件组合结构（Stack/Form/Layout）

## 4) QSS 职责边界
QSS 文件负责所有视觉样式，包括：
- 颜色
- 字体
- 边框
- 圆角
- padding/margin（组件视觉内外边距）
- hover / pressed / disabled / focus
- variant 的视觉表现（danger/warning/success/primary）

## 5) 禁止项
- 不要在组件 Python 代码中散落颜色、圆角、边框等视觉细节。
- 不要在组件内部大量使用 `setStyleSheet(...)` 写死样式。

## 6) 状态暴露约定（Property First）
组件应尽量通过 property 暴露状态，让 QSS 控制样式。
推荐属性：
- `kireiVariant`: `primary | subtle | danger | warning | success | ...`
- `kireiSize`: `compact | medium | large | ...`
- `kireiRole`: `title | text | input | password | ...`
- `kireiState`: `normal | loading | invalid | ...`

示例：
```python
self.setProperty("kireiVariant", "primary")
self.setProperty("kireiSize", "compact")
self.setProperty("kireiRole", "title")
self.setProperty("kireiState", "loading")
```

对应 QSS：
```qss
QPushButton[kirei="button"][kireiVariant="primary"] { ... }
QPushButton[kirei="button"][kireiSize="compact"] { ... }
QLabel[kireiRole="title"] { ... }
```

## 7) 用户覆盖机制
- KireiUI 提供默认 `base.qss`。
- 用户项目可以加载自己的 QSS 并放在后面，使其覆盖默认样式。
- 建议覆盖时优先使用相同 property 选择器（如 `[kireiVariant="primary"]`）保证语义一致。

推荐顺序：
1. 加载 KireiUI 内置 `base.qss`
2. 加载业务项目 `app.qss`（后加载覆盖前者）

## 8) 兼容性建议
- 历史属性（如 `variant`、`size`）可短期保留兼容。
- 新组件与新样式统一使用 `kirei*` 属性命名。
