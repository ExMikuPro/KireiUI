from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from kirei_ui import KireiText, KireiTitle  # noqa: E402
from kirei_ui.app import KireiApp, KireiWindow  # noqa: E402
from kirei_ui.desktop import KireiAction  # noqa: E402
from kirei_ui.icons import icon  # noqa: E402
from kirei_ui.inputs import KireiButton  # noqa: E402
from kirei_ui.layout import KireiCard, KireiHStack, KireiVStack  # noqa: E402
from kirei_ui.navigation import KireiSidebar  # noqa: E402
from kirei_ui.widgets.layout_plus import KireiToolbar  # noqa: E402


def resolve_theme_dirs() -> list[Path]:
    candidates = [
        ROOT / "styles" / "silicon_light",
        ROOT / "styles" / "aui_light",
        ROOT / "styles" / "eui_light",
    ]
    return [path for path in candidates if path.is_dir()][:1]


def main() -> int:
    app = KireiApp(qss_dirs=resolve_theme_dirs() or None)

    sidebar = (
        KireiSidebar()
        .add_item("Dashboard", "dashboard", icon="add")
        .add_item("Components", "components", icon="checkmark_circle", icon_style="filled")
        .add_item("Settings", "settings", icon="add")
        .current("dashboard")
    )

    toolbar = KireiToolbar()
    action_new = KireiAction("New").icon("add")
    action_done = KireiAction("Done").icon("checkmark_circle", style="filled")
    toolbar.add_action(action_new.qt_action()).add_action(action_done.qt_action())

    root = (
        KireiVStack()
        .padding(20)
        .spacing(12)
        .add(KireiTitle("KireiUI Fluent Icon Demo"))
        .add(KireiText("Regular/Filled icons, button icon API, sidebar and toolbar integration."))
        .add(
            KireiCard()
            .title("Button Icons")
            .content(
                KireiHStack()
                .spacing(10)
                .add(KireiButton("新增", icon="add"))
                .add(KireiButton("删除").icon("add", style="regular", size=20))
                .add(KireiButton("完成", icon=icon("checkmark_circle", style="filled", size=24)))
                .add(KireiButton(icon="add"))
            )
        )
        .add(
            KireiCard()
            .title("Icon Sizes")
            .content(
                KireiHStack()
                .spacing(10)
                .add(KireiButton("20 regular", icon="add", icon_size=20))
                .add(KireiButton("24 regular", icon="add", icon_size=24))
                .add(
                    KireiButton(
                        "24 filled",
                        icon="checkmark_circle",
                        icon_style="filled",
                        icon_size=24,
                    )
                )
            )
        )
        .add(KireiCard().title("Sidebar").content(sidebar))
        .add(KireiCard().title("Toolbar").content(toolbar))
    )

    window = KireiWindow().title("KireiUI Icon Demo").size(1000, 760).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
