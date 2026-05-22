# KireiUI 开发维护指南

## 1. 开发环境安装

```bash
pip install -e .
pip install -r requirements-dev.txt
```

## 2. 运行示例

```bash
python examples/hello_window.py
python examples/components_gallery.py
```

## 3. 添加新组件

建议流程：

1. 在 `src/kirei_ui/widgets/` 新建组件文件或扩展现有文件
2. 在对应分组模块导出（如 `inputs/__init__.py`）
3. 在 `src/kirei_ui/widgets/__init__.py` 与 `src/kirei_ui/__init__.py` 补导出
4. 添加测试
5. 更新文档

## 4. 新组件放置位置

- 输入类：`widgets/input.py`、`widgets/choice.py`、`widgets/select.py`
- 布局容器：`stack.py` 或 `widgets/layout_plus.py`
- 反馈类：`widgets/feedback.py`
- 弹层：`widgets/overlay.py`
- 桌面能力：`widgets/desktop.py`

## 5. API 设计规范（链式）

- 可配置方法返回 `Self`
- getter/setter 重载需保持直观
- 信号绑定方法以 `on_*` 命名
- 布尔语义方法建议支持默认值（如 `enabled(value=True)`）

## 6. 类型注解规范

- 对公开方法补全参数与返回类型
- callback 类型写明参数签名

## 7. docstring 规范

- 公开类与关键行为建议写简明 docstring
- 重点说明输入、返回、边界条件

## 8. QSS 命名规范

- 通用标识：`kirei`
- 角色：`kireiRole`
- 语义：`kireiVariant`
- 状态：`kireiState`
- 尺寸：`kireiSize`

## 9. 测试建议

- 链式返回值测试（`is self`）
- property 设置正确性测试
- 关键信号回调触发测试
- 主题构建顺序与覆盖测试

运行测试：

```bash
pytest
```

## 10. 提交前检查清单

```bash
ruff check src tests examples
black --check src tests examples
pytest
```

## 11. 文档更新策略

每次新增或修改公开 API 后，至少更新：

- `README.md`
- `docs/API_REFERENCE.md`
- `docs/COMPONENTS.md`（如涉及使用模式变化）
- `docs/THEMING.md`（如涉及样式机制变化）
