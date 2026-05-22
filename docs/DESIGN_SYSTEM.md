# KireiUI 设计系统

> 本文记录 KireiUI 已经在仓库内落地的视觉与交互约定。"建议"段落表示尚未在代码或 QSS 中完全统一的约束方向，会随版本逐步收敛。

## 设计目标

- 清晰：信息层级明确，状态可辨
- 稳定：组件外观与行为一致
- 克制：减少视觉噪音，强调任务效率
- 现代：适配工具型桌面应用

## 颜色 token

仓库当前已在 `styles/silicon_light/00_tokens.qss` 中定义参考 token（仅作设计参考，未通过 QSS 变量机制对外暴露，组件样式直接使用 hex）：

| 语义                | 值        |
| ------------------- | --------- |
| Page background     | `#F7F9FE` |
| Card background     | `#FFFFFF` |
| Weak background     | `#F1F4FC` |
| Primary             | `#6C7CFF` |
| Primary hover       | `#7F8DFF` |
| Primary pressed     | `#5868E8` |
| Blue                | `#4C8DFF` |
| Purple              | `#8A63FF` |
| Pink                | `#FF7AB6` |
| Success             | `#2AC78F` |
| Warning             | `#FFB020` |
| Danger              | `#FF5C7A` |
| Text                | `#1F2430` |
| Text secondary      | `#667085` |
| Text weak           | `#98A2B3` |
| Border              | `#DDE3F0` |
| Border weak         | `#E8ECF5` |

内置 `base.qss` 提供更中性的基础调色，主题化建议参考 `silicon_light` 的分层结构。

## 间距系统（建议基线）

推荐基线：`4 / 8 / 12 / 16 / 24 / 32px`

- 小控件内边距：4~8
- 表单行间距：8~12
- 区块间距：16~24
- 页面边距：24~32

KireiUI 不强制 token 名（如 `space.xs`），由具体组件 / 主题在 QSS 内自行落地。

## 圆角

- 默认 `4px`
- 卡片与面板可到 `6~8px`

## 字体层级

- `KireiTitle`：页面 / 区块主标题
- `KireiText`：正文说明
- `KireiLabel`：字段标签与辅助说明

通过 `kireiRole` 映射样式（`title / text / label`）。

## 阴影与边框

- 优先使用浅边框表达分层
- 阴影仅用于弹层、浮层、重要卡片

## 状态系统

通过 `kireiState` + Qt 伪状态联合表达：

- `hover` / `pressed` / `focused`：Qt 伪状态
- `disabled`：Qt 伪状态
- `checked` / `selected`：`kireiState="selected"` 等显式属性
- `loading` / `indeterminate` / `expanded` / `collapsed`：组件按需写入 `kireiState`

## 组件尺寸

- `KireiButton`：`compact | medium`
- 其它组件：尺寸 token 尚未在代码层统一（TODO）

> 后续目标是把所有支持尺寸语义的组件收敛到 `kireiSize` 上，并在 QSS token 层提供 `compact / medium` 的统一映射。

## 布局规范

- 页面主结构优先 `KireiVStack`
- 操作区常用 `KireiHStack + stretch`
- 复杂录入优先 `KireiForm`

## 表单规范

- 标签简洁明确
- 必填校验状态使用语义状态属性（如 `kireiState="error"`）
- 错误提示尽量贴近字段

## 按钮规范

- 主流程仅一个 primary
- 危险操作使用 `danger`
- 次要操作使用 `subtle / default`

## 面板与卡片

- `KireiPanel`：承载区域
- `KireiCard`：信息块 + 标题 / 描述 / 内容 / footer

## 图标

- 使用 `KireiIcon` / `icon(...)`，源为 Microsoft Fluent UI System Icons
- 风格在同一界面内保持一致（`regular` 或 `filled`）

## 空状态 / 错误状态 / 加载状态

- 空状态：`KireiEmpty`
- 错误提示：`KireiAlert().danger()`
- 进度或等待：`KireiProgress` / `KireiSpinner`

## 动画原则

- 默认短时、低干扰（`KireiApp.motion_duration` 默认 `180ms`）
- 优先任务反馈，不做炫技动画
- 动画开关全局可控（`KireiApp.enable_motion` / `set_motion_enabled(...)`）
- 单组件可覆盖（`KireiMotionMixin.animated(...)` / `animation_duration(...)`）

## 可访问性建议

- 保持足够对比度
- 键盘可达（Tab 顺序）
- Tooltip 作为图标按钮补充，不替代可见文案
- 颜色不作为唯一状态信号
