# Contributing to KireiUI

## 欢迎贡献

欢迎通过 Issue、Pull Request、文档改进、示例补充等方式参与 KireiUI。

## 你可以贡献什么

- 新组件与组件增强
- 主题与 QSS 改进
- 示例程序
- 测试
- 文档
- Bug 修复

## Issue 规范

请尽量包含：

- 复现步骤
- 预期行为
- 实际行为
- 环境信息（Python / PySide6 / OS）
- 最小复现代码（如可能）

## Pull Request 规范

- 一个 PR 聚焦一个主题
- 说明变更动机与影响范围
- 若改动公开 API，请同步更新文档
- 若改动样式机制，请提供示例或截图说明

## 代码风格

- Python 版本：`>=3.10`
- 格式化：`black`
- 规范检查：`ruff`
- 测试：`pytest`

## 文档风格

- 默认中文
- 术语保持一致：项目名统一 `KireiUI`，包名统一 `kirei_ui`
- 不伪造不存在 API

## 组件开发规范

- 类命名：`KireiXxx`
- 公开配置方法返回 `Self`
- 优先用 `setProperty` 暴露语义状态给 QSS
- 不在 Python 中硬编码视觉样式

## QSS 主题贡献规范

- 推荐使用 `kirei/kireiRole/kireiVariant/kireiState/kireiSize` 选择器
- 文件按层次组织（tokens/base/components/overrides）
- 保持状态样式完整（hover/focus/disabled 等）

## 示例贡献规范

- 示例必须能在仓库当前结构下运行
- 导入路径使用真实包名 `kirei_ui`
- 示例需说明用途和关键组件

## 提交前检查清单

```bash
ruff check src tests examples
black --check src tests examples
pytest
```

如变更了文档：

- [ ] `README.md` 已同步
- [ ] `docs/API_REFERENCE.md` 已同步
- [ ] `docs/COMPONENTS.md` / `docs/THEMING.md` 相关章节已同步
