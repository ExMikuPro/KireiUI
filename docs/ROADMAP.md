# KireiUI Roadmap

KireiUI 当前处于 **Pre-Alpha (0.1.x)**。下面用版本锚点记录已完成与计划中的工作，以便贡献者判断迭代节奏。

## 已完成（0.1.x）

### 应用层
- [x] `KireiApp` / `KireiWindow`
- [x] QSS 加载机制（`theme` / `qss_dirs` / `qss_files` / `recursive` / `extra_qss`）
- [x] 内置 `base.qss`
- [x] 全局 / 单组件动画开关（`KireiMotionMixin`、`KireiAnimator`）

### 布局
- [x] `KireiHStack` / `KireiVStack` / `KireiGrid` / `KireiForm`
- [x] `KireiScroll` / `KireiPanel` / `KireiSplitter` / `KireiStack` / `KireiTabs`

### 输入与文本
- [x] `KireiButton`（variant / size / loading / icon）
- [x] `KireiInput` / `KireiPassword` / `KireiTextarea`
- [x] `KireiCheckbox` / `KireiRadio` / `KireiSwitch`
- [x] `KireiComboBox`
- [x] `KireiSpinBox` / `KireiDoubleSpinBox` / `KireiSlider`
- [x] `KireiDateEdit` / `KireiTimeEdit` / `KireiDateTimeEdit`
- [x] `KireiLabel` / `KireiTitle` / `KireiText` / `KireiDivider`

### 反馈与展示
- [x] `KireiAlert` / `KireiBadge` / `KireiTag` / `KireiProgress` / `KireiSpinner` / `KireiEmpty`
- [x] `KireiCard` / `KireiSection`
- [x] `KireiTable` / `KireiList` / `KireiTree`
- [x] `KireiSearchBox` / `KireiFilterBar` / `KireiPagination`

### 导航与弹层
- [x] `KireiTopBar` / `KireiSidebar` / `KireiNavItem` / `KireiBreadcrumbs` / `KireiToolbar` / `KireiActionGroup` / `KireiMenu`
- [x] `KireiDialog` / `KireiConfirm` / `KireiMessageBox` / `KireiDrawer` / `KireiPopover` / `KireiTooltip`

### 桌面能力
- [x] `KireiAction` / `KireiShortcut` / `KireiMenuBar` / `KireiStatusBar` / `KireiSystemTray`
- [x] `KireiFileDialog` / `KireiColorDialog`

### 图标
- [x] Microsoft Fluent UI System Icons 集成（`KireiIcon` / `KireiIconRegistry` / `icon`）

### 工程
- [x] 主要公开 API 已覆盖类型注解
- [x] `tests/` 基础链式 / 行为测试（85+）
- [x] `examples/` 11 份运行示例

## 0.2 计划

- [ ] Toast / 浮层提示组件
- [ ] Dialog / Drawer 标准化的 `actions(...)` footer 构建器
- [ ] `KireiTokens` 升级为带语义层的 token 系统（颜色 / 间距 / 圆角 / 字号）
- [ ] 组件尺寸语义统一收敛到 `kireiSize`（当前仅 `KireiButton` 落地 `compact / medium`）
- [ ] 暗色主题 `dark.qss`
- [ ] 紧凑主题 `compact.qss`
- [ ] 全部组件 docstring 覆盖

## 0.3+ 计划

- [ ] 主题切换增强（运行时切换无闪烁、过渡动画）
- [ ] 动画 API 增强（更多预设、可组合的过渡）
- [ ] 可访问性改进（焦点环、ARIA 等价语义）
- [ ] 文档站点（mkdocs-material）
- [ ] 设计系统稳定（token / 组件状态语义冻结，进入 1.0 候选）

## 1.0 准入条件（草拟）

- 所有公开 API 在 0.x 区间内不再大改名 / 改签名
- token 系统稳定，dark / compact 主题落地
- 全部组件具备 docstring + 行为测试
- 文档站点上线，覆盖 API、组件、主题、设计系统