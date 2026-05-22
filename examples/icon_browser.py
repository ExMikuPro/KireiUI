from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from PySide6.QtCore import Qt  # noqa: E402
from PySide6.QtGui import QIcon  # noqa: E402
from PySide6.QtWidgets import (  # noqa: E402
    QApplication,
    QGridLayout,
    QLabel,
    QScrollArea,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from kirei_ui import KireiText, KireiTitle  # noqa: E402
from kirei_ui.app import KireiApp, KireiWindow  # noqa: E402
from kirei_ui.icons import KireiIconRegistry, icon  # noqa: E402
from kirei_ui.inputs import KireiButton  # noqa: E402
from kirei_ui.layout import KireiCard, KireiHStack, KireiVStack  # noqa: E402

COLUMNS = 20
ROWS = 10
PER_PAGE = COLUMNS * ROWS
ICON_STYLE = "regular"
ICON_SIZE = 24
BUTTON_SIZE = 36


def resolve_theme_dirs() -> list[Path]:
    candidates = [
        ROOT / "styles" / "silicon_light",
        ROOT / "styles" / "aui_light",
        ROOT / "styles" / "eui_light",
    ]
    return [path for path in candidates if path.is_dir()][:1]


class IconBrowser(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._names = KireiIconRegistry.names()
        self._page = 0
        self._page_count = max(1, math.ceil(len(self._names) / PER_PAGE))

        self._status = QLabel("Ready")
        self._page_label = QLabel("")

        self._grid_host = QWidget()
        self._grid = QGridLayout(self._grid_host)
        self._grid.setSpacing(6)
        self._grid.setContentsMargins(6, 6, 6, 6)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._grid_host)

        header = (
            KireiHStack()
            .spacing(8)
            .add(KireiButton("上一页").on_click(self._prev_page))
            .add(KireiButton("下一页").on_click(self._next_page))
            .add(KireiText(f"每页 {COLUMNS} x {ROWS} = {PER_PAGE} 个"))
        )

        layout = QVBoxLayout(self)
        layout.addWidget(
            KireiVStack()
            .spacing(8)
            .add(KireiTitle("KireiUI Fluent Icons Browser"))
            .add(
                KireiText(
                    "点击任意图标按钮会自动复制图标名称到剪切板, 支持分页浏览全部图标。"
                )
            )
            .add(header)
            .add(self._page_label)
            .add(self._status)
            .add(scroll)
        )

        self._render_page()

    def _render_page(self) -> None:
        while self._grid.count() > 0:
            item = self._grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        start = self._page * PER_PAGE
        end = min(len(self._names), start + PER_PAGE)
        page_names = self._names[start:end]

        for idx, name in enumerate(page_names):
            row = idx // COLUMNS
            col = idx % COLUMNS

            button = QToolButton()
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
            button.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
            button.setIconSize(button.size() - button.size() * 0.25)
            if KireiIconRegistry.exists(name, style=ICON_STYLE, size=ICON_SIZE):
                button.setIcon(icon(name, style=ICON_STYLE, size=ICON_SIZE, strict=False))
            else:
                button.setIcon(QIcon())
            button.setToolTip(name)
            button.clicked.connect(lambda _checked=False, n=name: self._copy_name(n))
            self._grid.addWidget(button, row, col)

        self._page_label.setText(
            f"第 {self._page + 1} / {self._page_count} 页 | 图标总数: {len(self._names)}"
        )

    def _copy_name(self, name: str) -> None:
        app = QApplication.instance()
        if app is None:
            return
        clipboard = app.clipboard()
        clipboard.setText(name)
        self._status.setText(f"已复制: {name}")

    def _prev_page(self) -> None:
        if self._page <= 0:
            return
        self._page -= 1
        self._render_page()

    def _next_page(self) -> None:
        if self._page >= self._page_count - 1:
            return
        self._page += 1
        self._render_page()


def main() -> int:
    app = KireiApp(qss_dirs=resolve_theme_dirs() or None)

    content = (
        KireiCard()
        .title("全图标按钮分页示例")
        .description("20x10 方形按钮网格, 点击复制名称。")
        .content(IconBrowser())
    )

    root = KireiVStack().padding(16).spacing(10).add(content)

    window = KireiWindow().title("KireiUI Icon Browser").size(1360, 900).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
