from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from PySide6.QtWidgets import QVBoxLayout, QWidget  # noqa: E402

from kirei_ui import KireiDivider, KireiText, KireiTitle  # noqa: E402
from kirei_ui.app import KireiApp, KireiWindow  # noqa: E402
from kirei_ui.feedback import KireiProgress  # noqa: E402
from kirei_ui.inputs import KireiButton, KireiSwitch  # noqa: E402
from kirei_ui.layout import (  # noqa: E402
    KireiCard,
    KireiHStack,
    KireiPanel,
    KireiVStack,
)
from kirei_ui.navigation import KireiSidebar  # noqa: E402
from kirei_ui.overlay import KireiDialog, KireiDrawer  # noqa: E402


def _resolve_theme_dirs() -> list[Path]:
    candidates = [
        ROOT / "styles" / "silicon_light",
        ROOT / "styles" / "aui_light",
        ROOT / "styles" / "eui_light",
    ]
    for path in candidates:
        if path.is_dir():
            return [path]
    return []


def _make_dialog() -> KireiDialog:
    body = KireiVStack().spacing(10).add(KireiText("This dialog demonstrates fade in/out."))
    dialog = KireiDialog().title("Animated Dialog").content(body).modal(True)
    close_bar = KireiHStack().stretch().add(
        KireiButton("Close animated").on_click(lambda: dialog.close_animated(animated=True))
    )
    dialog.footer(close_bar)
    return dialog


def _make_drawer() -> KireiDrawer:
    menu = (
        KireiVStack()
        .spacing(8)
        .add(KireiText("Drawer content with mock menu:"))
        .add(KireiButton("Overview"))
        .add(KireiButton("Projects"))
        .add(KireiButton("Settings"))
    )
    drawer = KireiDrawer().title("Motion Drawer").content(menu)
    return drawer


def _make_sidebar() -> KireiSidebar:
    return (
        KireiSidebar()
        .add_item("Dashboard", "dashboard")
        .add_item("Components", "components")
        .add_item("Settings", "settings")
        .add_item("About", "about")
        .current("dashboard")
    )


def main() -> int:
    qss_dirs = _resolve_theme_dirs()
    app = KireiApp(
        qss_dirs=qss_dirs or None,
        enable_motion=True,
        motion_duration=180,
    )

    motion_state = KireiText("Motion: Enabled")

    def update_motion_label() -> None:
        state = "Enabled" if app.enable_motion else "Disabled"
        motion_state.setText(f"Motion: {state}")

    dialog = _make_dialog()
    drawer = _make_drawer()
    sidebar = _make_sidebar()

    progress = KireiProgress().range(0, 100).text_visible(True).set_value(0, animated=False)
    component_default_off = (
        KireiProgress()
        .range(0, 100)
        .text_visible(True)
        .set_value(10, animated=False)
        .animated(False)
    )

    toggle_switch = KireiSwitch("Enable global motion").checked(True)

    def set_global_motion(enabled: bool) -> None:
        app.set_motion_enabled(enabled)
        update_motion_label()

    toggle_switch.on_change(set_global_motion)

    sidebar_card = (
        KireiCard()
        .title("Sidebar Collapse / Expand")
        .description("Use animated and instant toggle to compare motion behavior.")
        .content(
            KireiVStack()
            .spacing(10)
            .add(sidebar)
            .add(
                KireiHStack()
                .spacing(8)
                .add(KireiButton("Toggle sidebar animated").on_click(lambda: sidebar.toggle(True)))
                .add(KireiButton("Toggle sidebar instant").on_click(lambda: sidebar.toggle(False)))
            )
        )
    )

    root = (
        KireiVStack()
        .padding(20)
        .spacing(14)
        .add(KireiTitle("KireiUI Motion Demo"))
        .add(KireiText("Demonstrates global, component-level and per-call animation priority."))
        .add(KireiDivider())
        .add(
            KireiCard()
            .title("Global Motion Toggle")
            .description("Switch affects all motion-enabled components by default.")
            .content(KireiHStack().spacing(10).add(toggle_switch).add(motion_state))
        )
        .add(
            KireiCard()
            .title("Dialog Fade Demo")
            .description("Animated vs instant dialog show.")
            .content(
                KireiHStack()
                .spacing(8)
                .add(
                    KireiButton("Show animated dialog").on_click(
                        lambda: dialog.show_animated(True)
                    )
                )
                .add(
                    KireiButton("Show instant dialog").on_click(
                        lambda: dialog.show_animated(False)
                    )
                )
                .add(KireiButton("Close dialog").on_click(lambda: dialog.close_animated(True)))
            )
        )
        .add(
            KireiCard()
            .title("Drawer Slide Demo")
            .description("Open drawer with or without animation.")
            .content(
                KireiHStack()
                .spacing(8)
                .add(KireiButton("Open drawer animated").on_click(lambda: drawer.open(True)))
                .add(KireiButton("Open drawer instant").on_click(lambda: drawer.open(False)))
                .add(KireiButton("Close drawer").on_click(lambda: drawer.close(True)))
            )
        )
        .add(sidebar_card)
        .add(
            KireiCard()
            .title("Progress Smooth Demo")
            .description("Buttons animate to target; reset jumps instantly.")
            .content(
                KireiVStack()
                .spacing(8)
                .add(progress)
                .add(
                    KireiHStack()
                    .spacing(8)
                    .add(KireiButton("25%").on_click(lambda: progress.set_value(25, True)))
                    .add(KireiButton("50%").on_click(lambda: progress.set_value(50, True)))
                    .add(KireiButton("75%").on_click(lambda: progress.set_value(75, True)))
                    .add(KireiButton("100%").on_click(lambda: progress.set_value(100, True)))
                    .add(
                        KireiButton("Reset instant").on_click(
                            lambda: progress.set_value(0, False)
                        )
                    )
                )
            )
        )
        .add(
            KireiCard()
            .title("Priority Override Demo")
            .description("Method parameter animated > component animated > app enable_motion")
            .content(
                KireiVStack()
                .spacing(8)
                .add(KireiText("Component default: animated(False)"))
                .add(component_default_off)
                .add(
                    KireiHStack()
                    .spacing(8)
                    .add(
                        KireiButton("Default call (no anim)").on_click(
                            lambda: component_default_off.set_value(30)
                        )
                    )
                    .add(
                        KireiButton("Force animated").on_click(
                            lambda: component_default_off.set_value(80, True)
                        )
                    )
                    .add(
                        KireiButton("Force instant").on_click(
                            lambda: component_default_off.set_value(5, False)
                        )
                    )
                )
            )
        )
    )

    wrapper = QWidget()
    wrapper_layout = QVBoxLayout(wrapper)
    wrapper_layout.setContentsMargins(0, 0, 0, 0)
    wrapper_layout.addWidget(KireiPanel().content(root))

    window = KireiWindow().title("KireiUI Motion Demo").size(1100, 760).content(wrapper)
    window.show()
    update_motion_label()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
