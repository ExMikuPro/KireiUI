# KireiUI 主题系统（QSS）

## 为什么使用 QSS

KireiUI 选择 QSS，是为了把“视觉”与“结构/行为”分离：

- Python: 结构、状态、事件、组件组合
- QSS: 颜色、字号、间距、边框、hover/focus/disabled

这让 UI 更易维护，也便于项目级主题定制。

## 加载顺序

`KireiApp.set_theme(...)` 最终样式顺序：

1. 内置主题（`theme`，默认 `base`）
2. `qss_dirs`（按文件名排序加载）
3. `qss_files`
4. `extra_qss`

后加载内容会覆盖先加载内容。

## qss_dirs 的用途

- 批量加载一个主题目录下的多个 `.qss`
- 适合模块化组织样式（tokens/base/components/...）

```python
from pathlib import Path
from kirei_ui.app import KireiApp

app = KireiApp(qss_dirs=[Path("styles/silicon_light")])
```

## qss_files 的用途

- 精确指定若干文件
- 适合按需加载或局部覆盖

## recursive 参数

- `False`: 仅加载目录下一级 `.qss`
- `True`: 递归加载子目录 `.qss`

## extra_qss 的用途

- 快速注入小片段覆盖
- 适合实验、调试、动态主题微调

```python
app = KireiApp(extra_qss='QPushButton[kirei="button"] { border-radius: 8px; }')
```

## 推荐目录结构

```text
themes/
  default/
    tokens.qss
    base.qss
    components/
      button.qss
      input.qss
      panel.qss
      typography.qss
  dark/
    tokens.qss
    base.qss
    components/
      button.qss
      input.qss
      panel.qss
      typography.qss
```

仓库当前已有可参考目录：`styles/silicon_light/`。

## 推荐 QSS 分层

1. `tokens.qss`：颜色/间距/圆角约定（注释或变量化策略）
2. `base.qss`：全局基础样式
3. `components/*.qss`：组件级样式
4. `themes/*.qss`：主题差异覆盖

## 组件样式挂钩方式

### 1) objectName

```python
panel.object_name("main-panel")
```

```qss
#main-panel { border: 1px solid #d0d7de; }
```

### 2) dynamic property（推荐）

```python
button.setProperty("kireiVariant", "primary")
```

```qss
QPushButton[kirei="button"][kireiVariant="primary"] {
  background: #0052cc;
  color: white;
}
```

## Button Variant 样式示例

```qss
QPushButton[kirei="button"][kireiVariant="danger"] {
  background: #de350b;
  border: 1px solid #de350b;
  color: #fff;
}
```

## Dark Theme 示例思路

- 保持结构选择器不变（`[kirei=...]`）
- 仅替换颜色 token 和状态色
- 避免在 Python 分支判断深浅色

## 避免在 Python 写死颜色

不要：

```python
widget.setStyleSheet("color: #ff0000;")
```

建议：

- Python 仅设置语义状态（如 `kireiVariant="danger"`）
- QSS 决定视觉表现

## QSS 限制与动画边界

- QSS 不擅长复杂动画编排
- 复杂过渡建议用 `KireiMotionMixin + KireiAnimator` 或 Qt Animation API

## 主题开发最佳实践

1. 先定义语义 token，再映射到组件
2. 选择器尽量稳定（优先 `kirei*` property）
3. 组件样式拆文件并按编号控制顺序
4. 在示例页（如 `examples/components_gallery.py`）回归验证
5. 每次改主题时至少验证：按钮、输入、表单、导航、弹层、状态组件
